from __future__ import annotations
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class Test(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X, y = None) -> Test:
        return self

    def transform(self, X) -> pd.DataFrame:
        transformed_X = X.copy()
        print(transformed_X)
        return transformed_X
