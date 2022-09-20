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


## References
- [Machine Learning Engineering with MLflow]
- [Mlflow official documentation]
- [Accelerating the Machine Learning Lifecycle with MLflow]


[Machine Learning Engineering with MLflow]: https://github.com/PacktPublishing/Machine-Learning-Engineering-with-MLflow
[examples/stockpred]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/stockpred
[examples/02_docker_stack_example.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/02_docker_stack_example.ipynb
[examples/03_experiment_management_in_mlflow.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/03_experiment_management_in_mlflow.ipynb
[examples/04_managing_models_with_mlflow.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/04_managing_models_with_mlflow.ipynb
[Accelerating the Machine Learning Lifecycle with MLflow]: https://cs.stanford.edu/~matei/papers/2018/ieee_mlflow.pdf
[Mlflow official documentation]: https://www.mlflow.org/docs/latest/index.html
