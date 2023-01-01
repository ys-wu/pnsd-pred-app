from io import StringIO
import pickle

import numpy as np
import pandas as pd
import tensorflow as tf

import config


def parse(file):
    try:
        data = file.read().decode("utf-8")
        df = pd.read_csv(StringIO(data), parse_dates=[config.DATETIME_NAME])
        df.set_index(config.DATETIME_NAME, inplace=True)
        df.astype("float32")
        return df
    except:
        return None


def load_models():
    scaler_x = pickle.load(open(config.SCALER_X_PATH, 'rb'))
    scaler_y = pickle.load(open(config.SCALER_Y_PATH, 'rb'))
    model = tf.keras.models.load_model(config.MODEL_PATH)
    return scaler_x, scaler_y, model


def _predict(X, scaler_x, scaler_y, model):
    X_scaled = scaler_x.transform(X)

    x = []
    for i in range(X_scaled.shape[0] - config.LOOKBACK + 1):
        x.append(X_scaled[i: i + config.LOOKBACK])

    Y_pred = model.predict(np.array(x))
    Y_pred_rescaled = pd.DataFrame(
        data=scaler_y.inverse_transform(Y_pred),
        index=X.index[config.LOOKBACK -1:],
        columns=config.SIZES, 
    )

    return Y_pred_rescaled


def predict(file):
    X = parse(file)
    scaler_x, scaler_y, model = load_models()
    return _predict(X, scaler_x, scaler_y, model)
