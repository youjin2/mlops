import os
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
        train_run = _run("train_model")
        # _run("evaluate_model")

        # model_uri = os.path.join(train_run.info.artifact_uri, "model")
        # _run("register_model", parameters={"model_uri": model_uri})


if __name__ == "__main__":
    workflow()
