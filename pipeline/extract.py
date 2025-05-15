import re
import pandas as pd

LOG_PATH = 'data/logfiles.log'
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

if __name__ == "__main__":
    df = parse_logs(LOG_PATH)
    print(df.head())
