## Goal
[MLflow] is a open source platform that manages the machine learning model lifecycle including experimentation, reproducibility and deployment.  
In this tutorial, you can see how `BentoML` and `MLflow` pipeline can be integrated together.

## Setup Workbench
```bash
$ cd examples/mlflow_integration

$ docker-compose build
$ docker images
$ docker-compose up -d
```

## Run MLflow experiment
```bash
$ cd examples/mlflow_integration

$ mlflow run project/ --experiment-name mlflow-tensorflow-mnist --env-manager local
```


## References
- [mlflow introduction]
- [bentoml/examples/mlflow]


[mlflow introduction]: https://github.com/youjin2/mlops/tree/main/mlflow
[bentoml/examples/mlflow]: https://github.com/bentoml/BentoML/tree/main/examples/mlflow/
[MLflow]: https://www.mlflow.org/
