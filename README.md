# fittEd backend

> By Ivan Sowerby, Fanhua Huang, Dhyey Mehta, Benedek Labancz,  Dimitri Bonneville, Marcus Gupta

> use Python>=3.10.11

## Introduction

Our submission for Hack The Burgh XII, introducing fittEd - a framework and platform for rapidly optimising ML pipelines, and making the use of them easy and effective.

With a performant, extensive backend API for real-time dataset preprocessing and modelling dynamically for labels from varying features, and an intuitive BUI (Browser User Interface) webpage for encouraging tinkering with pipelines and their respective hyperparameters across domains to understand their applications.

### Making sense of fittEd

The main fittEd program consists of many isolated services/modules that work together to compose a functional API for versatile datasets and ML pipelines to be shared, tinkered on/with, and understood.

---

## Setup

### Main (backend API):

1. `cd` to the root of the backend directory
2. Install with `./scripts/install.ps1` (Windows) or `./scripts/install.sh` (Unix-based)
3. Run with `./scripts/server.ps1` (Windows) or `./scripts/server.sh` (Unix-based)

Additional (for contributions):

4. Build before pushing with `./scripts/build.ps1` (Windows) or `./scripts/build.sh` (Unix-based)

---

### Real-time Test

1. `cd` to the root of the backend directory 
2. Run with `./scripts/test.ps1` (Windows) or `./scripts/test.sh` (Unix-based)

---

### Local Webpage

1. Ensure NPM is installed with `npm --version`
2. `cd` to the app folder immediately under the frontend directory
3. Build with `npm i`
4. Run with `npm run dev` and navigate to the port on `http://localhost` that the webpage is hosted on

---

## API Documentation

Our backend relies on the FastAPI Python library for handling HTTP requests from the front-end.

### Making Requests

Our API offers four endpoints to make requests to.

1. `POST "/dataset/create"`
Send the contents of a CSV file as raw text to the backend to parse. The dataset is saved and a unique ID is generated, which makes future operations on datasets quick and minimises data traffic.

2. `GET "/dataset/get"`
Similar to `dattaset/create`, except that data flows in the opposite direction.

3. `GET "/session/delete"`
Deleting a dataset from the storage at the backend.

4. `POST "/label"`
This is the main operation to perform on a dataset. The backend expects a `LabelRequest` from the frontend:
```python
class LabelRequest(BaseModel):
    session_id: str
    features: dict
    config: dict
```

The `features` describe a datapoint with some available values and some missing values (specified as None).
The `config` gives the blueprint for the ML workload to perform to train a model and make predictions of the missing values in the given datapoint.

The request returns a dictionary with a key `fields`, same as `features` but with predictions added, and `score`, which is a performance metric computed against the test dataset.

---

## Labeller Documentation

Labeller is an machine learning system that predicts missing fields in data. 

### 1. Load Complete Database
The system stores the full dataset with all fields to use as training data for future predictions.

### 2. Receive Partial Data
When the user sends data with some fields missing, the system automatically detects which fields are provided and which are absent.

### 3. Dynamic Model Training
Creates and trains a scikit-learn pipeline using:
- **Provided fields** as input features (X)
- **Missing fields** as prediction targets (y)

### 4. Model Caching
Trained models are cached using a unique key based on the field combination. If the user requests the same combination again, it reuses the cached model instead of retraining.

### 5. Return Complete Data
Predictions are merged back with the user's input data, returning a complete DataFrame with all fields filled in, along with a performance score.

## Configuration Structure

The Labeller is configured through a JSON dictionary with two main sections:

### 1. Preprocessing
Array of transformation steps applied sequentially before the model. Each step specifies:
- Class name from `sklearn.preprocessing` (e.g., StandardScaler, PolynomialFeatures)
- Constructor arguments as key-value pairs

### 2. Model
The final estimator that makes the actual predictions. Supports:
- Any class from `sklearn.linear_model` (LinearRegression, Ridge, Lasso, etc.)
- Any class from `sklearn.ensemble` (RandomForestRegressor, GradientBoostingRegressor, etc.)
- Any class from `sklearn.neural_network` (MLPRegressor, etc.)

#### Example Configuration 1 (linear regression)
```json
{
    "preprocessing": [
        {
            "name": "PolynomialFeatures",
            "args": 
            {
                "degree": 2,
                "include_bias": false
            }
        },
        {
            "name": "StandardScaler",
            "args": {}
        }
    ],
    "model": 
    {
        "name": "LinearRegression",
        "args": {}
    }
}
```

#### Example Configuration 2 (multi-layered perceptron)
``` json
{
    "preprocessing": [
        {"name": "StandardScaler", "args": {}}
    ],
    "model": {
        "name": "MLPRegressor",
        "args": {
            "hidden_layer_sizes": [100, 50],
            "random_state": 42
        }
    }
}
```

### External Modules/Packages

`requirements.txt`:
``` python
annotated-doc==0.0.3
annotated-types==0.7.0
anyio==4.11.0
certifi==2025.10.5
charset-normalizer==3.4.4
click==8.3.0
colorama==0.4.6
dnspython==2.8.0
email-validator==2.3.0
exceptiongroup==1.3.0
fastapi==0.120.4
fastapi-cli==0.0.14
fastapi-cloud-cli==0.3.1
h11==0.16.0
httpcore==1.0.9
httptools==0.7.1
httpx==0.28.1
idna==3.11
Jinja2==3.1.6
joblib==1.5.2
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
numpy==2.2.6
pandas==2.3.3
pydantic==2.12.3
pydantic_core==2.41.4
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
python-multipart==0.0.20
pytz==2025.2
PyYAML==6.0.3
requests==2.32.5
rich==14.2.0
rich-toolkit==0.15.1
rignore==0.7.3
scikit-learn==1.7.2
scipy==1.15.3
sentry-sdk==2.43.0
shellingham==1.5.4
six==1.17.0
sniffio==1.3.1
starlette==0.49.3
termcolor==3.2.0
threadpoolctl==3.6.0
typer==0.20.0
typing==3.7.4.3
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
uvicorn==0.38.0
watchfiles==1.1.1
websockets==15.0.1
```

---

# fittEd frontend

## App

The frontend of this project is made with **SvelteKit** and **Supabase**

In Supabase, there is a table called `data`, which contains the following fields:

- id: the unique primary key
- created_at: the time at which it was created
- user_id: this ID is the unique UUID of the user who created this row
- session: this is the key that will be used to communicate with the python server
- name: this is the name of a project

In order to use the application, the user needs to:

1. Make an account with their email and a password
2. Create a project with a CSV file
3. The program will give the user options to select which fields to predict and select values for the remaining fields
4. The program will give the user an option to put a link that links to a configuraton file, which can lead to different machine learning analysis.
5. After fetching from the Python API, it will set the values of predicted values with the prediction, and display the accuracy
6. Role-level security on Supabase was enabled such that only authenticated users can create new entries to data, and that a user can only select and remove an entry whose user_id field is equal to the user's UUID

There is a dashboard when the user is logged in:

1. The user can create new projects
2. The user can search within their existing projects
3. The user can delete their projects

### The Python API

The backend APIs written in Python will be used to perform analysis. Whenever a new project is made, the CSV file will be uploaded to the Python API, and the Python API will return a session ID, which the app will store in supabase.
`
### Styling

The styling is done with **Tailwind CSS, daisyUI, and SVG.js**. A custom theme in daisyUI was used along with some custom css classes to improve visuals. SVG components, especially paths, were used to feature a more data-focused vibe.

### Use of AI

Due to time constraints, _Claude Sonnet 4.5_ was used to format the html elements with styling, making the SVG paths glow and have gradient color. The rest of the decorations and the overall website are not generated by AI.

Some program files are based on the Supabase Documentation from https://supabase.com/docs/guides/auth/server-side/sveltekit

### External Modules/Packages

`package.json`:
```json
{
	"name": "app",
	"private": true,
	"version": "0.0.1",
	"type": "module",
	"scripts": {
		"dev": "vite dev",
		"build": "vite build",
		"preview": "vite preview",
		"prepare": "svelte-kit sync || echo ''",
		"check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
		"check:watch": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --watch",
		"format": "prettier --write .",
		"lint": "prettier --check . && eslint ."
	},
	"devDependencies": {
		"@eslint/compat": "^1.4.0",
		"@eslint/js": "^9.38.0",
		"@sveltejs/adapter-auto": "^7.0.0",
		"@sveltejs/kit": "^2.47.1",
		"@sveltejs/vite-plugin-svelte": "^6.2.1",
		"@tailwindcss/vite": "^4.1.14",
		"@types/node": "^22",
		"daisyui": "^5.3.11",
		"eslint": "^9.38.0",
		"eslint-config-prettier": "^10.1.8",
		"eslint-plugin-svelte": "^3.12.4",
		"globals": "^16.4.0",
		"prettier": "^3.6.2",
		"prettier-plugin-svelte": "^3.4.0",
		"prettier-plugin-tailwindcss": "^0.7.1",
		"svelte": "^5.41.0",
		"svelte-check": "^4.3.3",
		"tailwindcss": "^4.1.14",
		"typescript": "^5.9.3",
		"typescript-eslint": "^8.46.1",
		"vite": "^7.1.10"
	},
	"dependencies": {
		"@supabase/ssr": "^0.7.0",
		"@supabase/supabase-js": "^2.78.0",
		"@svgdotjs/svg.js": "^3.2.5"
	}
}
```
