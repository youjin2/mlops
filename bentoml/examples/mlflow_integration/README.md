## Goal
[MLflow] is a open source platform that manages the machine learning model lifecycle including experimentation, reproducibility and deployment.  
In this tutorial, you can see how `BentoML` and `MLflow` pipeline can be integrated together.

## Setup Workbench
To resolve [tensorflow autologging issue], you may have to upgrade the tensorflow version.
```bash
$ cd examples/mlflow_integration

$ docker-compose build
$ docker images
$ docker-compose up -d
$ docker exec -it workbench-jupyter /bin/bash

# upgrade tensorflow version
$ pip install tensorflow-gpu==2.8
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
[tensorflow autologging issue]: https://github.com/tensorflow/tensorflow/issues/54286
