import pandas as pd
from sklearn.model_selection import train_test_split
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_data_path():
    if os.path.exists("/app/data/processed_data.csv"):
        return "/app/data/processed_data.csv"
    else:
        return "data/processed_data.csv"
    
def prepare_data():
    data_path = get_data_path()
    df = pd.read_csv(data_path)

    X = df.drop(["response_time"], axis=1)
    y = df["response_time"]

    return train_test_split(X, y, test_size=0.2, random_state=42)