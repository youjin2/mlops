## End-to-end MLflow pipeline example
docker based MLflow project example
- build docker image
    ```bash
    $ cd mlflow/
    $ docker-compose build
    ```
- use pre-built `mlflow-image` docker image in this exampe
- project description
    - `dataset`: Yahoo Finance dataset
        - contains high, low, open, close values of the stock price
        - our target is whether delta(=close-open) is greater than zero or not
    - `goal`: stock market movement detection
    - `model`: scikit-learn's `RandomForestClassifier`
    - see `./train.py` for code details
- run project
    ```bash
    $ cd mlflow/examples/stockpred/
    $ mlflow run .
    ```
- change hyperparameters & run project again with command above

## MLflow tracking
- run mlflow ui
    ```bash
    $ cd mlflow/

    # run docker-conatiner
    $ docker-compose up -d
    $ docker exec -it mlflow /bin/bash

    # run mlflow webserver (note that container:5000 is binded at host:5000)
    $ cd ./examples/stockpred/
    $ mlflow ui --host 0.0.0.0 --port 5000

    # mlflow webserver is available at http//xxx.xxx.xxx.xxx:5000
    ```
- mlflow webserver is available at `http//your.host.ip.addr:5000`
- you can see two experimental results!
- also, MLflow tracking allows comparing results between different runs


## Exploring MLflow Models
- serve saved ml models
    ```bash
    # run below command in docker-container
    # change port if mlflow webserver is running
    $ mlflow models serve -m ./mlruns/0/da21caeea5f342e3b507b9a86e6c0651/artifacts/model_random_forest/ --host 0.0.0.0 --port 5000
    ```
- after conda env created, get model prediction with following command
    ```bash
    # request model preiction
    $ curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json' -d '{"data":[[1,1,1,1,0,1,1,1,0,1,1,1,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0]] }'

    # reponse was [1, 0]
    ```
