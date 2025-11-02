from typing import Union
from label import *
# from util import *
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uuid
from pathlib import Path
import os
import time
from datetime import datetime, timedelta
import asyncio
from io import StringIO

# SESSION_DIR.mkdir(parents=True, exist_ok=True)
SESSION_DIR = Path('data/pickles/')

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server started.")
    yield
    print("Server shutting down.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/dataset/create")
async def create_dataset(request: Request) -> dict:
    body_bytes = await request.body()    
    text_content = body_bytes.decode('utf-8')
    dataset_id = str(uuid.uuid4())
    
    try:
        csvStringIO = StringIO(text_content)
        df = pd.read_csv(csvStringIO, sep=",")
    except:
        raise HTTPException(500, "Parsing input file failed.")
    
    # Save as pickle (more efficient than pickle for dataframes)
    path = SESSION_DIR / (dataset_id + ".pickle")
    df.to_pickle(path)
    
    return {"session_id": dataset_id}

def pickle_path(session_id: str) -> Path:
    return SESSION_DIR / (session_id + ".pickle")

@app.get("/dataset/get")
def get_dataset(session_id: str) -> str:
    path = pickle_path(session_id)

    if not path.exists():
        raise HTTPException(404, "Dataset not found")
    
    df = pd.read_pickle(path)
    body = df.to_csv(index = False)
    return Response(
        content = body,
        media_type = 'text/csv'
    )

class LabelRequest(BaseModel):
    session_id: str
    features: dict
    config: dict

@app.get("/session/delete")
def delete_session(session_id: str) -> dict:
    path = pickle_path(session_id)
    try:
        os.remove(path)
    except:
        raise HTTPException(404, "Dataset not found.")
    return {"status": "success"}

class LabelRequest(BaseModel):
    session_id: str
    features: dict
    config: dict

@app.post('/label')
def label(
    request: LabelRequest
) -> dict:
    path = pickle_path(request.session_id)

    if not path.exists():
        raise HTTPException(404, "Dataset not found")
    
    df = pd.read_pickle(path)
    
    labeller = Labeller(request.config)
    labeller.load_database(df)

    partial_data = pd.DataFrame(
        {key: value for (key, value) in request.features.items() if value != None}
    )
    result, score = labeller.predict(partial_data)
    from json import dumps as json_dumps
    body = json_dumps({
        'fields': result.to_csv(index = False),
        'score': score
    })
    return Response(
        content = body,
        media_type = 'application/json'
    )
