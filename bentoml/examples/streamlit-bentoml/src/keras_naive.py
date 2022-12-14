import shutil
import os

import mlflow

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Dense,
    Dropout,
)
from tensorflow.keras.constraints import non_neg
from tensorflow.keras.callbacks import EarlyStopping

from .utils import (
    set_mlflow_crendentials,
    get_metadata,
    mean_squared_error,
    mean_absolute_error,
)


def get_keras_naive(num_features):
    inputs = Input(shape=(num_features,))
    x = inputs
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.3)(x)
    x = Dense(32, activation="relu")(x)
    outputs = Dense(1, kernel_constraint=non_neg())(x)

    model = Model(inputs, outputs)
    model.compile(optimizer="adam", loss="mse")

    return model


if __name__ == "__main__":
    set_mlflow_crendentials()

    # load dataset
    (X_train, y_train), (X_valid, y_valid) = get_metadata(train_valid_split=True)
    num_features = X_train.shape[1]

    # build model
    model = get_keras_naive(num_features)
    es_callback = EarlyStopping(patience=5)

    # run mlflow experiment
    mlflow.set_experiment("Pawpularity Score")
    with mlflow.start_run(run_name="keras_mlp"):
        model_dir = "./tmp/keras_naive"
        model.fit(
            X_train, y_train,
            batch_size=64,
            epochs=100,
            validation_data=(X_valid, y_valid),
            callbacks=[es_callback]
        )
        model.save(model_dir)

        pred_train = model.predict(X_train)
        pred_valid = model.predict(X_valid)

        print(f"Train MSE: {mean_squared_error(y_train, pred_train)}")
        print(f"Test MSE: {mean_squared_error(y_valid, pred_valid)}")

        # log metrics manually
        # current version of tensorflow does not supports the mlflow.autolog()
        metrics = {
            "training_mae": mean_absolute_error(y_train, pred_train),
            "training_mse": mean_squared_error(y_train, pred_train, squared=True),
            "training_rmse": mean_squared_error(y_train, pred_train, squared=False),
            "valid_mae": mean_absolute_error(y_valid, pred_valid),
            "valid_mse": mean_squared_error(y_valid, pred_valid, squared=True),
            "valid_rmse": mean_squared_error(y_valid, pred_valid, squared=False),
        }
        mlflow.log_metrics(metrics)

        # log model to mlflow tracking server
        mlflow.tensorflow.log_model(
            tf_saved_model_dir=model_dir,
            tf_meta_graph_tags=["serve"],
            tf_signature_def_key="serving_default",
            artifact_path="keras_naive",
        )

        # remove local saved model once logged to the mlflow tracking server
        shutil.rmtree(os.path.dirname(model_dir))
