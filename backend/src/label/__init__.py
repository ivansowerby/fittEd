from enum import Enum
from typing import Callable, Dict, List, Any, Optional
import numpy as np
import pandas as pd
import sklearn.preprocessing as preprocessing
import sklearn.linear_model as linear_model
import sklearn.ensemble as ensemble
from sklearn.pipeline import Pipeline
# import util

class LabellerEnum(list, Enum):
    PREPROCESSING_TYPE = [
        preprocessing,
        # util
    ]
    MODEL_TYPE = [
        linear_model,
        ensemble
    ]

    def is_member(_type, instance: str) -> Callable|None:
        for module in _type.value:
            if not hasattr(module, instance): continue
            callable = getattr(module, instance)
            return callable
        return None

class Labeller:
    """
    Main system that loads from JSON config and handles predictions.
    Front-end just sends data with missing fields, system figures out the rest!
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Load configuration from dict"""
        self.config = config
        self.trained_models: Dict[str, Pipeline] = {}
        self.train_data: Optional[pd.DataFrame] = None
        self.test_data: Optional[pd.DataFrame] = None
        self.all_fields: List[str] = []
    
    def _create_pipeline(self) -> Pipeline:
        """Create a fresh sklearn pipeline from the config"""
        steps = []

        def add_step(enumerable: tuple) -> None:
            i, step = enumerable
            class_name = step['name']
            step_class = LabellerEnum.PREPROCESSING_TYPE.is_member(class_name)
            print(step_class)
            if step_class:
                class_key, kwargs = f'{class_name}_{i}', step['args']
                # kwargs = .set_output(transform="pandas")
                _class = step_class(**kwargs)
                steps.append(
                    (class_key, _class)
                )
        
        # for i, step in enumerate(self.config["preprocessing"]):
        #     class_name = step["name"]
            
        #     step_class = LabellerEnum.PREPROCESSING_TYPE.is_member(class_name)
        #     if step_class:
        #         steps.append((f"{class_name}_{i}", step_class(**step["args"])))
        map(add_step, enumerate(self.config['preprocessing']))

        model_name = self.config["model"]["name"]
        
        # if hasattr(linear_model, model_name):
        #     model_class = getattr(linear_model, model_name)
        # elif hasattr(ensemble, model_name):
        #     model_class = getattr(ensemble, model_name)
        model_class = LabellerEnum.MODEL_TYPE.is_member(model_name)
        if not model_class:
            raise ValueError(f"Model class '{model_name}' not found in sklearn.linear_model or sklearn.ensemble")
        
        steps.append(("model", model_class(**self.config["model"]["args"])))
        
        return Pipeline(steps)
    
    def load_database(self, data: pd.DataFrame):
        """Load complete database for training."""
        self.all_fields = list(data.columns)
        self.train_data = data.copy()
        self.test_data = pd.DataFrame()
    
    def _train_model(self, features: List[str], labels: List[str]) -> Pipeline:
        """Train a model for a specific feature/label split"""
        if self.train_data is None:
            raise ValueError("Must load complete database first!")
        
        model_key = f"{','.join(sorted(features))}_to_{','.join(sorted(labels))}"
        
        if model_key in self.trained_models:
            return self.trained_models[model_key]
        
        X_train = self.train_data[features].values
        y_train = self.train_data[labels].values
        
        if len(labels) == 1:
            y_train = y_train.ravel()
        
        pipeline = self._create_pipeline()
        pipeline.fit(X_train, y_train)
        
        score = pipeline.score(X_train, y_train)

        self.trained_models[model_key] = pipeline

        return pipeline, score
    
    def predict(self, partial_data: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        """
        Main API endpoint: pass partial data, get complete data back.
        Missing fields are automatically detected and predicted.
        """
        result = partial_data.copy()
        
        provided_fields = []
        missing_fields = []
        
        for field in self.all_fields:
            if field in partial_data.columns:
                if partial_data[field].notna().any():
                    provided_fields.append(field)
                else:
                    missing_fields.append(field)
            else:
                missing_fields.append(field)
        
        if not missing_fields:
            return result
        
        if not provided_fields:
            raise ValueError("No provided fields, cannot predict!")
        
        pipeline, score = self._train_model(provided_fields, missing_fields)
        
        X = partial_data[provided_fields].values
        predictions = pipeline.predict(X)
        
        if len(missing_fields) == 1:
            result[missing_fields[0]] = predictions
        else:
            for i, field in enumerate(missing_fields):
                result[field] = predictions[:, i]
        
        return result, score

if __name__ == "__main__":
    from sklearn.linear_model import LinearRegression
    print(
        LabellerEnum.MODEL_TYPE.is_member('LinearRegression')
    )

    complete_db = pd.DataFrame({
        'age': [25, 30, 35, 40, 45, 50, 55, 60, 28, 33],
        'years_experience': [2, 5, 8, 12, 15, 20, 25, 30, 4, 8],
        'education_level': [1, 2, 2, 3, 3, 3, 4, 4, 2, 2],
        'salary': [50000, 65000, 75000, 90000, 95000, 110000, 120000, 130000, 58000, 70000],
        'hours_per_week': [45, 45, 50, 50, 45, 40, 40, 35, 48, 50],
    })
    
    config = {
        "preprocessing": [
            {
                "name": "Test",
                "args": {}
            },
            {
                "name": "PolynomialFeatures",
                "args": {
                    "degree": 2,
                    "include_bias": False
                }
            },
            {
                "name": "StandardScaler",
                "args": {}
            }
        ],
        "model": {
            "name": "LinearRegression",
            "args": {}
        }
    }
    
    ml_system = Labeller(config)
    
    ml_system.load_database(complete_db)
    
    print("\n" + "="*60)
    print("SCENARIO 1: Predict salary and hours")
    user_input_1 = pd.DataFrame({
        'age': [29, 42],
        'years_experience': [5, 14],
        'education_level': [2, 3],
    })
    
    result_1, score_1 = ml_system.predict(user_input_1)
    print(result_1)
    
    # print("\n" + "="*60)
    # print("SCENARIO 2: Predict age and experience")
    # user_input_2 = pd.DataFrame({
    #     'salary': [80000, 115000],
    #     'hours_per_week': [48, 42],
    #     'education_level': [2, 3],
    # })
    
    # result_2, score_2 = ml_system.predict(user_input_2)
    # print(result_2)

# .set_output(transform="pandas")