import json
import os

import bentoml
import mlflow

from .utils import mlflow_credential_path


EXPERIMENT_NAME = "Pawpularity Score"
BETNO_SAVE_NAME = "keras-conv2d-model"


def set_credentials():
    # read mlflow credentials
    with open(mlflow_credential_path, "r") as f:
        credentials = json.load(f)

    # set mlflow accounts
    os.environ["MLFLOW_TRACKING_USERNAME"] = credentials["MLFLOW_TRACKING_USERNAME"]
    os.environ["MLFLOW_TRACKING_PASSWORD"] = credentials["MLFLOW_TRACKING_PASSWORD"]


def get_latest_conv2d_run():
    # get all mlflow runs with given experiment_name
    runs = mlflow.search_runs(experiment_names=[EXPERIMENT_NAME])

    # filter conv2d models
    conv2d_runs = runs.\
        query("`tags.mlflow.runName` == 'keras_conv2d'").\
        query("status == 'FINISHED'").\
        sort_values("end_time", ascending=False)

    latest_log_model_history = json.loads(
        conv2d_runs["tags.mlflow.log-model.history"].iloc[0]
    )[0]

    return latest_log_model_history


def save_bento_model():
    latest_log_model_history = get_latest_conv2d_run()
    latest_model_uri = os.path.join(
        "runs:",
        latest_log_model_history["run_id"],
        latest_log_model_history["artifact_path"]
    )
    bentoml.mlflow.import_model(BETNO_SAVE_NAME, latest_model_uri)


if __name__ == "__main__":
    save_bento_model()
