## MLflow practices

Most of the examples are based on [Machine Learning Engineering with MLflow].


### End-to-end MLflow pipeline
Use `docker-compose-demo.yml` to build docker-based simple end-to-end MLflow pipeline.  
See [examples/stockpred], which develops a classificiation model to detect stock market movement with MLflow.  
You can also check out the `MLflow trackinig` component which is the webserver providing visual explanations of different model runs and ML model serving examples with `mlflow models serve`.


### Machine Learning Project Process
1. Ideation: identifying a business opportunity & formulating the problem
2. Prototyping: verifying the feasibility
3. Pilot: evaluating and iterating over a ML algorithm
4. Production: run the ML project in production


### Build MLflow workbench with docker stack
development docker stack based MLflow workbench, which consists of following components.
* Docker/Docker compose: handle each of the main component dependencies of the architecture
* Jupyter: develops data science code and analytics in the context of machine learning
* MLflow: provides facilities for experiment tracking, model management, registry, and deployment interface
* PostgresSQL: part of the architecture at this stage, as the storage layer for MLflow for backend metadata

i) build workbench components with docker stack.
```bash
# build jupyter/mlflow/postgres docker images
$ docker-compose build

# run docker MLflow stack
$ docker-compose up -d
```

ii) run ML experiments on local jupyter and check the results on the MLflow server.  
ML experiment Examples can be found at
- [examples/02_docker_stack_example.ipynb]: check docker stack workbench with dummy ML pipeline.
- [examples/03_experiment_management_in_mlflow.ipynb]: practical example using different ML frameworks.  
(scikit-learn, xgboost, keras)


## References
- [Machine Learning Engineering with MLflow]
- [Mlflow official documentation]
- [Accelerating the Machine Learning Lifecycle with MLflow]


[Machine Learning Engineering with MLflow]: https://github.com/PacktPublishing/Machine-Learning-Engineering-with-MLflow
[examples/stockpred]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/stockpred
[examples/02_docker_stack_example.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/02_docker_stack_example.ipynb
[examples/03_experiment_management_in_mlflow.ipynb]: https://github.com/youjin2/mlops/tree/main/mlflow/examples/03_experiment_management_in_mlflow.ipynb
[Accelerating the Machine Learning Lifecycle with MLflow]: https://cs.stanford.edu/~matei/papers/2018/ieee_mlflow.pdf
[Mlflow official documentation]: https://www.mlflow.org/docs/latest/index.html
