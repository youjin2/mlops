import mlflow


if __name__ == "__main__":
    with mlflow.start_run(run_name="register_model") as run:
        mlflow.set_tag("mlflow.runName", "register_model")

        model_uri = run.data.params["model_uri"]
        result = mlflow.register_model(
            model_uri,
            "training-model-pystock",
        )
