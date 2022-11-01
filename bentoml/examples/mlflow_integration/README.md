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

# run docker-stack workbench
$ docker-compose up -d
$ docker exec -it workbench-jupyter /bin/bash

# run mlflow experiments
$ mlflow run project/ --experiment-name mlflow-tensorflow-mnist --env-manager local
```

After MLflow pipeline finished, you can check out the result:
```
$ cd examples/mlflow_integration
$ tree project/ -d

project/
├── bentoml
│   ├── bentos
│   └── models
│       ├── keras
│       │   └── b3rcxesz4cmikasc
│       │       ├── ...
│       ├── keras_native
│       │   └── bx6hpksz4cmikasc
│       │       ├── ...
│       └── mlflow_keras
│           └── bzxk7asz4cmikasc
│               └── mlflow_model
│                   └── ...
├── models
│   ├── ...
└── src
    └── ...
```



## References
- [mlflow introduction]
- [bentoml/examples/mlflow]


[mlflow introduction]: https://github.com/youjin2/mlops/tree/main/mlflow
[bentoml/examples/mlflow]: https://github.com/bentoml/BentoML/tree/main/examples/mlflow/
[MLflow]: https://www.mlflow.org/
[tensorflow autologging issue]: https://github.com/tensorflow/tensorflow/issues/54286
