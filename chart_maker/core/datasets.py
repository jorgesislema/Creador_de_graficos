# datasets.py
# Módulo para manejar datasets de ejemplo o cargados por el usuario

import pandas as pd
from typing import Dict

def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def get_example_datasets() -> Dict[str, str]:
    return {
        "iris": "datasets/iris.csv",
        "cars": "datasets/cars.csv"
    }
