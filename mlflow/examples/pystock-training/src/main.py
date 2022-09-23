import os

import mlflow
import click


def _run(entrypoint, parameters={}, source_version=None, use_cache=True):
    # existing_run = _already_ran(entrypoint, parameters, source_version)
    # if use_cache and existing_run:
    #     print("Found existing run for entrypoint=%s and parameters=%s" % (entrypoint, parameters))
    #     return existing_run
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
    with mlflow.start_run(run_name="pystock-training"):
        mlflow.set_tag("mlflow.runName", "pystock-training")
        train_run = _run("train_model")
        _run("evaluate_model")

        model_uri = os.path.join(train_run.info.artifact_uri, "model")
        # mlflow.register_model(
        #     model_uri,
        #     "training-model-psystock"
        # )
        # check passing model_uri to entrypoint
        _run("register_model", parameters={"model_uri": model_uri})


if __name__ == "__main__":
    workflow()
