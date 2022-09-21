import pandas as pd
import mlflow
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    jaccard_score,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    zero_one_loss,
)


def classification_metrics(df: pd.DataFrame):

    y_test = df["y_test"]
    y_pred = df["y_pred"]

    metrics = {}
    metrics["accuracy_score"] = accuracy_score(y_test, y_pred)
    metrics["average_precision_score"] = average_precision_score(y_test, y_pred)
    metrics["f1_score"] = f1_score(y_test, y_pred)
    metrics["jaccard_score"] = jaccard_score(y_test, y_pred)
    metrics["log_loss"] = log_loss(y_test, y_pred)
    metrics["matthews_corrcoef"] = matthews_corrcoef(y_test, y_pred)
    metrics["precision_score"] = precision_score(y_test, y_pred)
    metrics["recall_score"] = recall_score(y_test, y_pred)
    metrics["zero_one_loss"] = zero_one_loss(y_test, y_pred)
    return metrics


if __name__ == "__main__":
    with mlflow.start_run(run_name="evaluate_model") as run:
        mlflow.set_tag("mlflow.runName", "evaluate_model")
        df = pd.read_csv("data/predictions/test_predictions.csv")
        metrics = classification_metrics(df)
        mlflow.log_metrics(metrics)
