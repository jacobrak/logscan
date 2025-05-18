import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data():
    df = pd.read_csv("data/processed_data.csv")

    X = df.drop(["response_time"], axis=1)
    y = df["response_time"]

    return train_test_split(X, y, test_size=0.2, random_state=42)