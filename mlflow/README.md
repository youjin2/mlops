## MLflow practices
Most of the examples are based on [Machine Learning Engineering with MLflow].


## End-to-end MLflow pipeline
Use `docker-compose-demo.yml` to build docker-based simple end-to-end MLflow pipeline.  
See [examples/stockpred], which develops a classificiation model to detect stock market movement with MLflow.  
You can also check out the `MLflow trackinig` component which is the webserver providing visual explanations of different model runs and ML model serving examples with `mlflow models serve`.


## Machine Learning Project Process
1. `Ideation`: identifying a business opportunity & formulating the problem
2. `Prototyping`: verifying the feasibility
3. `Pilot`: evaluating and iterating over a ML algorithm
4. `Production`: run the ML project in production


## Build MLflow workbench with docker stack
development docker stack based MLflow workbench, which consists of following components.
* `Docker/Docker compose`: handle each of the main component dependencies of the architecture
* `Jupyter`: develops data science code and analytics in the context of machine learning
* `MLflow`: provides facilities for experiment tracking, model management, registry, and deployment interface
* `PostgresSQL`: part of the architecture at this stage, as the storage layer for MLflow for backend metadata

i) build workbench components with docker stack.
```bash
# build jupyter/mlflow/postgres docker images
$ docker-compose build

# run docker MLflow stack
$ docker-compose up -d
```

ii) run ML experiments on local jupyter and check the results on the MLflow server.  
ML experiment Examples can be found at
- [examples/02_docker_stack_example.ipynb]: check docker stack workbench with dummy ML pipeline
- [examples/03_experiment_management_in_mlflow.ipynb]: practical example using different ML frameworks  
(scikit-learn, xgboost, keras)


## Managing Models with MLflow
On the MLflow platform, there are two main components available to manage models.
- `Models`: manages the format, library, and standards enforcement module on the platform and  
supports a variety of the most used ML models (sklearn, XGBoost, TensorFlow, ...)
- `Model Registry`: handles a model life cycle, from registering and tagging model metadata  
so it can be retrieved by relevant systems

The central piece of the definition of MLflow models is the MLflow model file,
```yaml
artifact_path: model
flavors:
  python_function:
    env: conda.yaml
    loader_module: mlflow.sklearn
    model_path: model.pkl
    python_version: 3.10.6
  sklearn:
    code: null
    pickled_model: model.pkl
    serialization_format: cloudpickle
    sklearn_version: 1.1.2
mlflow_version: 1.28.0
model_uuid: af380c2cbc4844b1b31cc4a40c085c43
run_id: 97ee9e6938aa4ea7a1ef9fef30f634db
signature:
  inputs: '[{"type": "tensor", "tensor-spec": {"dtype": "int64", "shape": [-1, 14]}}]'
  outputs: '[{"type": "tensor", "tensor-spec": {"dtype": "int64", "shape": [-1]}}]'
utc_time_created: '2022-09-19 14:43:00.353762'
```
- `run_id`: reference to the run of the model
- `time_created`: timestamp of when the model was created
- `flavors`: different types of models, whether that is the native models (TensorFlow, Keras, sklearn, and so on)  
supported by MLflow or the pyfunc model provided by MLflow
- `signature`: component of the MLmodel that defines the signature and inferences process of the model,  
also it allows the validation of input data that needs to match the signature of the model

A model life cycle can undergo the following stages
- `Development`: exploring and trying out different approaches
- `Staging`: can be tested automatically with production- type traffic
- `Production`: ready to handle real-life production traffic
- `Archive`: no longer serves the business purpose that it was initially developed for

Detailed example can be found at [examples/04_managing_models_with_mlflow.ipynb]


## Training Models with MLflow
Now that you have created a docker stack workbench, let's run ML pipeline including train/evaluation/deploy steps.  
Example ML project is composed as following structure. (see [examples/pystock-training])  
```bash
├── conda.yaml
├── data
│   ├── predictions
│   │   └── test_predictions.csv
│   └── training
│       └── data.csv
├── MLProject
└── src
    ├── evaluate_model.py
    ├── __init__.py
    ├── main.py
    ├── register_model.py
    └── train_model.py
```

`MLproject` defines the entire ML pieline as below.
```yaml
name: pystock_training
conda_env: conda.yaml
entry_points:
  main:
    data_file: path
    command: "python -m src.main"
  train_model:
    command: "python -m src.train_model"
  evaluate_model:
    command: "python -m src.evaluate_model"
  register_model:
    command: "python -m src.register_model"
```

Let's run docker-based ML pipeline with MLflow
```bash
$ cd mlflow/

# run workbench
$ docker-compose up -d

# run ML pipeline
$ docker exec -it mlflow-jupyter /bin/bash
$ cd examples/pystock-training/
$ mlflow run . --experiment-name example-pystock-training --env-manager local

# once pipeline finished, go to MLflow UI (http://"your_ip_address":5000)
# - Experiments tab: you can see that "example-pystock-training" is created (see each run components for more details)
# - Models tab: you can see that "training-model-psystock" is created and "Version 1" deployed
```


## Deployment and Inference with MLflow
**i) Batch inference**  
A docker image provides you with a mechanism to run your batch scoring job in any environment supporting Docker images.  
(see [examples/pystock-serving/pystock-inference-batch])
```bash
# first, run mlflow-server with our docker stack workbench
$ cd mlflow/
$ docker-compose up -d mlflow

# create "pystock-inference-batch" docker image
$ cd mlflow/examples/pystock-serving/pystock-inference-batch/
$ docker-compose build

# run batch inference pipeline
# NOTE: mlflow-serving container shares a existing network with our workbench
# (use "mlflow_default" network which is our workbench's network name)
$ docker-compose run --rm batch-serving

# FYI: container's network can be identified by
$ docker ps --format '{{ .ID }} {{ .Names }} {{ json .Networks }}'
```

**ii) API server**  
Setting up an dockerized API system by relying on the MLflow built-in REST API environment.  
(see [examples/pystock-serving/pystock-inference-api])
```bash
# first, run mlflow-server with our docker stack workbench 
$ cd mlflow/
$ docker-compose up -d mlflow

# create "pystock-inference-api" docker image
$ cd mlflow/examples/pystock-serving/pystock-inference-api/
$ docker-compose build

# run api server with the Production model
$ docker-compose up -d
$ mlflow models serve -m "models:/training-model-pystock/Production" --env-manager local --host 0.0.0.0 --port 12000

# run command below on your local machine and check the API response
# expected output: [0.8296052813529968, 0.8817128539085388] (depends on your model)
$ curl http://127.0.0.1:12000/invocations -H 'Content-Type: application/json' -d '{"data":[[1,1,1,1,0,1,1,1,0,1,1,1,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0]] }'
# or
$ curl http://0.0.0.0:12000/invocations -H 'Content-Type: application/json' -d '{"data":[[1,1,1,1,0,1,1,1,0,1,1,1,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0]] }'
```


## References
- [Machine Learning Engineering with MLflow]
- [Mlflow official documentation]
- [Accelerating the Machine Learning Lifecycle with MLflow]


[Machine Learning Engineering with MLflow]: https://github.com/PacktPublishing/Machine-Learning-Engineering-with-MLflow
[examples/stockpred]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/stockpred
[examples/02_docker_stack_example.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/02_docker_stack_example.ipynb
[examples/03_experiment_management_in_mlflow.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/03_experiment_management_in_mlflow.ipynb
[examples/04_managing_models_with_mlflow.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/04_managing_models_with_mlflow.ipynb
[examples/pystock-training]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/pystock-training
[examples/pystock-serving/pystock-inference-batch]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/pystock-serving/pystock-inference-batch
[examples/pystock-serving/pystock-inference-api]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/pystock-serving/pystock-inference-api
[Accelerating the Machine Learning Lifecycle with MLflow]: https://cs.stanford.edu/~matei/papers/2018/ieee_mlflow.pdf
[Mlflow official documentation]: https://www.mlflow.org/docs/latest/index.html
