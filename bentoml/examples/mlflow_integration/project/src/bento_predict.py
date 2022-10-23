import json

import numpy as np
import mlflow
import bentoml
import tensorflow as tf

from .train import load_dataset


def main():
    # search previous runs
    # NOTE: experiment ids may vary
    runs = mlflow.search_runs(experiment_names=["mlflow-tensorflow-mnist"]).\
        sort_values("start_time", ascending=False)

    # get latest run_id & artifact_path
    run_id = runs.run_id.iloc[0]
    model_tag = json.loads(
        mlflow.get_run(run_id).data.tags["mlflow.log-model.history"]
    )
    artifact_path = model_tag[0]["artifact_path"]

    # model uri
    model_uri = f"runs:/{run_id}/{artifact_path}"

    model = tf.keras.models.load_model("./tmp_model/")
    # option 1: directly save trained model to BentoML
    model_1 = bentoml.keras.save_model("keras_native", model)
    print(f"BentoML model imported as keras native: {model_1}")

    # option 2:
    model_2 = bentoml.mlflow.import_model("mlflow_keras", model_uri)
    print(f"BentoML model imported as mlflow pyfunc: {model_2}")

    # option 3:
    # loaded_model = mlflow.keras.load_model(model_uri)
    # model_3 = bentoml.keras.save_model("keras_native", loaded_model)

    bentoml_models = [
        model_1,
        model_2,
        # model_3,
    ]

    *_, (X_test, y_test) = load_dataset()
    for bento_model in bentoml_models:
        runner = bento_model.to_runner()
        runner.init_local()
        breakpoint()

        assert np.allclose(runner.predict.run(X_test), model.predict(X_test))


if __name__ == "__main__":
    main()
