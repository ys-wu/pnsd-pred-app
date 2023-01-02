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


def combine_bins_dNdlogDp(df, Dp_ranges=[[0, 2.5e-6]], out_type='N'):
#     print("Input dN/dlogDp, unit in (#/cm3)")

    def Dp_range2text(Dp_range, out_type):
        return out_type + '.' + str(Dp_range[0]) + "to" + str(Dp_range[1])

    Dp = np.array(df.columns, dtype="float")
    logDp = np.log10(Dp)
    delta_Dp = np.diff(logDp)
    dlogDp = np.append(delta_Dp[0], (delta_Dp[:-1]+delta_Dp[1:])/2)
    dlogDp = np.append(dlogDp, delta_Dp[-1])
    
    df = df.apply(lambda x: x*dlogDp, axis=1) # dN
    index_list = [(df.columns>Dp_range[0]) & \
                  (df.columns<=Dp_range[1]) for Dp_range in Dp_ranges]

    index = df.index

    if out_type == "N":
        print(f"Output type: {out_type}, unit: #/cm3")
        columns = [Dp_range2text(Dp_range, out_type) for Dp_range in Dp_ranges]
        data = np.transpose(
            np.stack([df[df.columns[index]].sum(axis=1, skipna=False).values \
                      for index in index_list]))
        return pd.DataFrame(index=index, columns=columns, data=data)

    elif out_type == "S":
        print(f"Output type: {out_type}, unit: um2/cm3")
        columns = [Dp_range2text(Dp_range, out_type) for Dp_range in Dp_ranges]
        bin_surface = np.pi*(Dp**2)*1e12
        df = df.apply(lambda x: x*bin_surface, axis=1)
        data = np.transpose(
            np.stack([df[df.columns[index]].sum(axis=1, skipna=False).values \
                      for index in index_list]))
        return pd.DataFrame(index=index, columns=columns, data=data)

    elif out_type == "V":
        print(f"Output type: {out_type}, unit: um3/cm3")
        columns = [Dp_range2text(Dp_range, out_type) for Dp_range in Dp_ranges]
        bin_volumn = (np.pi/6)*(Dp**3)*1e18
        df = df.apply(lambda x: x*bin_volumn, axis=1)
        data = np.transpose(
            np.stack([df[df.columns[index]].sum(axis=1, skipna=False).values \
                      for index in index_list]))
        return pd.DataFrame(index=index, columns=columns, data=data)

    else:
        print("Choose one of these as output type: N(numbe), S(surface), V(volumn)")
        raise


def predict(file):
    X = parse(file)
    scaler_x, scaler_y, model = load_models()
    df_pred = _predict(X, scaler_x, scaler_y, model)
    df_Ntot = combine_bins_dNdlogDp(df_pred)
    return df_Ntot
