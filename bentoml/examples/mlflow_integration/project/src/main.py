import click

import mlflow


def _run(entrypoint, parameters={}, source_version=None, use_cache=True):
    print("Launching new run for entrypoint=%s and parameters=%s" % (entrypoint, parameters))
    submitted_run = mlflow.run(
        ".",
        entrypoint,
        parameters=parameters,
        env_manager="local"
    )

    return mlflow.tracking.MlflowClient().get_run(submitted_run.run_id)


@click.command()
def workflow():
    with mlflow.start_run(run_name="mlflow_pipeline"):
        mlflow.set_tag("mlflow.runName", "mnist-training")
        _run("train_model")
        _run("bento_predict")


if __name__ == "__main__":
    workflow()
