import re
import pandas as pd
import random
import numpy as np
from user_agents import parse
import os
def get_data_path():
    if os.path.exists("/app/data/logfiles.log"):
        return "/app/data/logfiles.log"
    else:
        return "data/logfiles.log"

def get_data_path2():
    if os.path.exists("/app/data/"):
        return "/app/data/processed_data.csv"
    else:
        return "data/processed_data1.csv"
    
LOG_PATH = get_data_path()
LOG_PATTERN = r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<endpoint>\S+) HTTP/\d\.\d" (?P<status>\d+) (?P<bytes>\d+) "(?P<referrer>[^"]+)" "(?P<ua>[^"]+)" (?P<response_time>\d+)'

def drop_data(df):
    """
    Drop unnessacry data
    
    * Time - Only one time
    * Referrer - Only one url
    """
    return df.drop(["time", "referrer"], axis=1)

def parse_logs(path):
    data = []
    with open(path) as f:
        for line in f:
            match = re.match(LOG_PATTERN, line)
            if match:
                data.append(match.groupdict())
    
    return drop_data(pd.DataFrame(data))

def recreate(df: pd.DataFrame) -> pd.DataFrame:
    # Mapping dictionaries
    method_map = {
        "GET": 0,
        "DELETE": 1,
        "PUT": 2,
        "POST": 3
    }

    method_map2 = {
        "/usr": 0,
        "/usr/register": 1,
        "/usr/admin": 2,
        "/usr/admin/developer": 3,
        "/usr/login": 4
    }

    # Parse user-agent
    ua_parsed = df["ua"].apply(parse)
    df["os"] = ua_parsed.apply(lambda x: x.os.family)
    df["device"] = ua_parsed.apply(lambda x: x.device.family)
    df["browser"] = ua_parsed.apply(lambda x: x.browser.family)

    # Encode method and endpoint
    df["request_type_dummy"] = df["method"].map(method_map)
    df["endpoint_dummy"] = df["endpoint"].map(method_map2)

    # Status conversion and error flag
    df["status"] = df["status"].astype(int)
    df["is_error"] = (df["status"] >= 400).astype(int)

    # One-hot encoding
    os_dummies = pd.get_dummies(df['os'], prefix='os', drop_first=True).astype(int)
    device_dummies = pd.get_dummies(df['device'], prefix='d', drop_first=True).astype(int)
    browser_dummies = pd.get_dummies(df['browser'], prefix='b', drop_first=True).astype(int)

    # Set seeds
    random.seed(42)
    np.random.seed(42)

    # Concatenate dummies
    df = pd.concat([df, os_dummies, device_dummies, browser_dummies], axis=1)

    # Create synthetic response time
    df["response_time"] = (
        df["bytes"].astype(int) // 11 +
        df["request_type_dummy"].astype(int) * np.random.normal(25, 25, len(df)) +
        df["endpoint_dummy"].astype(int) * 15 +
        df.get("os_Mac OS X", 0) * np.random.normal(80, 10, len(df)) +
        df.get("os_Windows", 0) * np.random.normal(90, 10, len(df)) +

        df.get("d_Mac", 0) * np.random.normal(100, 15, len(df)) +
        df.get("d_iPhone", 0) * np.random.normal(120, 20, len(df)) +
        df.get("d_Other", 0) * -np.random.normal(160, 20, len(df)) +

        df.get("b_Chrome Mobile", 0) * np.random.normal(75, 15, len(df)) +
        df.get("b_Edge", 0) * np.random.normal(195, 25, len(df)) +
        df.get("b_Edge Mobile", 0) * -np.random.normal(165, 25, len(df)) +
        df.get("b_Opera", 0) * np.random.normal(90, 15, len(df)) +
        df.get("b_Safari", 0) * np.random.normal(110, 20, len(df)) +
        df.get("b_Opera Mobile", 0) * -90 +
        df["request_type_dummy"].astype(int) * df["endpoint_dummy"].astype(int) * 25 +
        np.random.normal(0, 100, len(df))  # general noise
    )

    # Drop unnecessary columns
    df = df.drop(["ip", "method", "endpoint", "ua", "os", "device", "browser", "status"], axis=1)

    return df

def save_clean_dataframe():
    df = parse_logs(LOG_PATH)
    new_df = recreate(df)
    file_path = get_data_path2()
    new_df.to_csv(file_path, index=False)

if __name__ == "__main__":
    df = parse_logs(LOG_PATH)
    print(df.head())
