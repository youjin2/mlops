import mlflow
from sklearn.ensemble import RandomForestRegressor

from .utils import (
    set_mlflow_crendentials,
    get_metadata,
    mean_squared_error
)


def get_sklearn_baseline():

    model = RandomForestRegressor(
        n_estimators=1500,
        random_state=1234,
        max_depth=5,
        n_jobs=-1,
        min_samples_split=3,
        max_features="sqrt",
    )

    return model


if __name__ == "__main__":
    set_mlflow_crendentials()

    (X_train, y_train), (X_test, y_test) = get_metadata(train_valid_split=True)
    model = get_sklearn_baseline()

    mlflow.set_experiment("Pawpularity Score")
    mlflow.sklearn.autolog()
    with mlflow.start_run(run_name="sklearn_baseline"):
        model.fit(X_train, y_train)
        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)

        print(f"Train MSE: {mean_squared_error(y_train, pred_train)}")
        print(f"Test MSE: {mean_squared_error(y_test, pred_test)}")
