from backend.enum import BackendEnum
from data.enum import Data
from configs.enum import ConfigsEnum
import pandas as pd
from json import loads as json_loads, dumps as json_dumps
from asyncio import run as async_run
from live import subscribe as subscribe_bitcoin
import requests
from io import StringIO
from math import floor
from termcolor import colored

def create_dataset(dataset: pd.DataFrame) -> str|None:
    """
    POST
    """
    headers = {
        'Content-Type': 'text/plain'
    }
    body = dataset.to_csv(index = False)
    endpoint = BackendEnum.API_URL.endpoint(
        'dataset/create'
    )
    response = requests.post(
        endpoint,
        data = body,
        headers = headers
    )
    if response.ok:
        response = response.json()
        session_id = response['session_id']
        return session_id
    return None

def get_dataset(session_id: str) -> pd.DataFrame|None:
    """
    GET
    """
    endpoint = BackendEnum.API_URL.endpoint(
        'dataset/get'
    )
    body = {'session_id': session_id}
    response = requests.get(
        endpoint,
        params = body
    )
    if response.ok:
        textIO = StringIO(response.text)
        dataset = pd.read_csv(textIO, sep=",")
        return dataset
    return None

def delete_session(session_id: str) -> bool:
    """
    GET
    """
    endpoint = BackendEnum.API_URL.endpoint(
        'session/delete'
    )
    body = {'session_id': session_id}
    response = requests.post(
        endpoint,
        params = body
    )
    return response.ok

def label(
        session_id: str,
        features: dict,
        config: dict
    ) -> tuple[dict, float]|None:
    """
    POST
    """
    endpoint = BackendEnum.API_URL.endpoint(
        'label'
    )
    body = {
        'session_id': session_id,
        'features': features,
        'config': config
    }
    response = requests.post(
        endpoint,
        json = body
    )
    if response.ok:
        print(colored('> Successfully Labelled!', 'green'))
        response = json_loads(response.text)
        textIO = StringIO(response['fields'])
        fields = pd.read_csv(textIO, sep=",")
        return (
            fields,
            response['score']
        )
    print(colored('> Failed Labelling', 'red'))
    return None

if __name__ == '__main__':
    FIELDS = ['n_tx', 'size', 'weight']
    BITCOIN_DATASET = pd.read_csv(
        Data.BitcoinEnum.PATH.value
    )[FIELDS]
    print(colored('Training on:', 'blue'))
    print(BITCOIN_DATASET)
    print()
    linear_regression_config = {}
    with open(ConfigsEnum.LINEAR_REGRESSION_PATH.value, 'r') as file:
        linear_regression_config = json_loads(file.read())
    
    session_id = create_dataset(BITCOIN_DATASET)
    print(f'{colored("Session ID", "yellow")}: {session_id}')

    def callback(block) -> None:
        fields = {field: None for field in FIELDS}
        fields['n_tx'] = [block['nTx']]
        print()
        print(colored('-'*20, 'grey'))
        print()
        outcome = label(
            session_id,
            fields,
            linear_regression_config
        )
        if outcome:
            fields, score = outcome
            print(colored('Live Inference:', 'blue'))
            print(fields.astype(int))
            accuracy = str(floor(score * 10_000)).zfill(4)
            percentage = str(int(accuracy[:2])) + '.' + accuracy[2:]
            print(f'=> Accuracy: {colored(percentage + "%", "blue")}')
    
    if session_id:
        #test
        async_run(subscribe_bitcoin(
            callback
        ))
    # delete_session(session_id)
