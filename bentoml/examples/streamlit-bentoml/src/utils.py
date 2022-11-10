import os
import json

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from .configs import (
    train_meta_path,
    # test_meta_path,
    mlflow_credential_path,
    parent_dir,
)


def set_mlflow_crendentials():
    with open(mlflow_credential_path, "r") as f:
        credentials = json.load(f)
    os.environ["MLFLOW_TRACKING_USERNAME"] = credentials["MLFLOW_TRACKING_USERNAME"]
    os.environ["MLFLOW_TRACKING_PASSWORD"] = credentials["MLFLOW_TRACKING_PASSWORD"]


def get_metadata(train_valid_split=True, seed=1234):
    train_data = pd.read_csv(train_meta_path)
    # test_data = pd.read_csv(configs.test_meta_path)

    if train_valid_split:
        train_data, valid_data = train_test_split(train_data, test_size=0.1, random_state=seed)
    else:
        valid_data = pd.DataFrame(columns=train_data.columns)

    def get_input_output(data: pd.DataFrame):
        data = data.copy()
        X_data = data.drop(["Id", "Pawpularity"], axis=1)
        y_data = data[["Pawpularity"]]
        return (X_data, y_data)

    X_train, y_train = get_input_output(train_data)
    X_valid, y_valid = get_input_output(valid_data)
    # X_test, y_test = get_input_output(test_data)

    return (X_train, y_train), (X_valid, y_valid)
    # return (X_train, y_train), (X_valid, y_valid), (X_test, y_test)


def get_conv2d_metadata(train_valid_split=True, seed=1234):
    train_data = pd.read_csv(train_meta_path)
    # test_data = pd.read_csv(configs.test_meta_path)

    if train_valid_split:
        train_data, valid_data = train_test_split(train_data, test_size=0.1, random_state=seed)
    else:
        valid_data = pd.DataFrame(columns=train_data.columns)

    def get_input_output(data: pd.DataFrame):
        X_data = data["Id"].apply(
            lambda x: os.path.join(parent_dir, "petfinder/data/raw/train", f"{x}.jpg")
        ).values
        y_data = data["Pawpularity"].values
        return (X_data, y_data)

    X_train, y_train = get_input_output(train_data)
    X_valid, y_valid = get_input_output(valid_data)

    return (X_train, y_train), (X_valid, y_valid)


def mean_squared_error(y_true, y_pred, squared=False):
    y_true = np.reshape(np.array(y_true), -1)
    y_pred = np.reshape(np.array(y_pred), -1)

    mse = np.nanmean((y_pred - y_true)**2)
    if not squared:
        mse = mse**(1/2.)

    return mse


def mean_absolute_error(y_true, y_pred):
    y_true = np.reshape(np.array(y_true), -1)
    y_pred = np.reshape(np.array(y_pred), -1)

    mae = np.nanmean(np.abs(y_true - y_pred))

    return mae


if __name__ == "__main__":
    set_mlflow_crendentials()
    get_metadata()
    print(os.environ)
