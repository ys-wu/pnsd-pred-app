from io import StringIO
import pandas as pd


def parse(file):
    try:
        data = file.read().decode("utf-8")
        df = pd.read_csv(StringIO(data))
        return df
    except:
        return None
