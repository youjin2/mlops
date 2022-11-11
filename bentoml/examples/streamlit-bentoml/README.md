## Goal
In this example, we will train and deploy the `Keras image regression model` to predict the cutiness score of cats and dogs using `Pet Pawpularity dataset` on Kaggle.  
Also, we will cover various MLOps & data version control services descibed below to manage the machine learning pipeline and finally we will use `streamlit` & `bentoml` to interact with the developed model on web UI.
- [DagsHub]
- [DVC]
- [MLflow]
- [BentoML]
- [Streamlit]
- [Heroku]


## Setup Dependencies
### Python environment
We use [pre-built bentoml docker image] as a base python development environment for this example.  
Additional dependencies (`mlflow`, `dagshub`, `dvc`, ...) are specified in [examples/streamlit-bentoml/requirements.txt] and they are automatically installed while running `docker-compose up`.
```bash
$ cd examples/streamlit-bentoml/
$ docker-compose up -d
$ docker exec -it bentoml-serving /bin/bash
```

### DagsHub & DVC
First, create your dagshub repository. (e.g. `https://dagshub.com/{your_dagshub_username}/petfinder`)  
(Note that it is like github for data scienists and machine learning engineers.)

After creating remote respository on dagshub, clone the repository on your local environment.
```bash
$ cd ./bentoml/examples/
$ git clone https://dagshub.com/{your_dagshub_username}/petfinder.git ./petfinder/
```

Once you finished to setup python environment described above, you can run `dvc` on command line interface.  
Below is code examples on how to use `dvc` & `dagshub` for data version control on CLI.

```bash
$ cd ./petfinder/

# init dvc (NOTE: dvc remote is {repo_name}.dvc, not {repo_name}.git)
$ dvc init
$ dvc remote add origin https://dagshub.com/{your_dagshub_username}/petfinder.dvc
$ dvc remote modify origin --local auth basic
$ dvc remote modify origin --local user {your_dagshub_username}
$ dvc remote modify origin --local password {your_dagshub_password}

# commit dvc init result
$ git add .dvc/ .dvcignore .gitignore
# you may have to add below line to "./dvc/config" to call "dvc get" to download data later
# [core]
#     remote = origin
$ git commit -m "ENH: init DVC"
$ git push origin main

# download dataset from my repo
$ dvc get https://dagshub.com/youjin2/petfinder data

# add data for dvc version control
$ dvc add data/
$ git add data.dvc .gitignore
$ git commit -m "ENH: dvc add data for version control"

# push dataset to dagshub storage
$ dvc push -r origin
$ git push origin main
```

### Git Submodule
`Dagshub` repo can be specified as a git submodule. (see below)
```bash
# init & push submodule history
$ cd examples/streamlit-bentoml/
$ git submodule add https://dagshub.com/youjin2/petfinder.git
$ git commit -m "ENH: add dagshub petfinder submodule"
$ git push origin main

# if any changes happen to remote submodule
$ git submodule update
```


### MLflow on DagsHub
`MLflow` is an open source platform that manages the machine learning lifecycle.  
`Dagshub` supports the `MLflow` tracking server (web UI managing ML experiments) and we will use this to manage experiments on this project.  

First, change the `MLFLOW_TRACKING_URI` specified in the `examples/streamlit-bentoml/.env` to your dagshub (or other appropriate) mlflow tracking uri.  
In my case, `MLFLOW_TRACKING_URI` is setted to `https://dagshub.com/youjin2/petfinder.mlflow`.

And then, put `credentials.json` to `examples/streamlit-bentoml` as below.  
Otherwise, mlflow tracking server will not be able to find the credential information.
```json
{
    "MLFLOW_TRACKING_USERNAME": "{your_dagshub_username}",
    "MLFLOW_TRACKING_PASSWORD": "{your_dagshub_password}"
}
```



## Train Pawpularity Predictinon models
You need to set environment variables about credential information.  
Export the shell variables by typing below line on CLI inside the docker container.
```bash
$ cd examples/streamlit-bentoml/
$ export MLFLOW_TRACKING_USERNAME={your_dagshub_username}
$ export MLFLOW_TRACKING_PASSWORD={your_dagshub_password}
```

I made three models to predict `Pawpularity` score and you can run & log the experiments by running commands below in the docker container.  
(See `examples/streamlit-bentoml/MLProject` for detailed description about entrypoints)
```bash
$ cd examples/streamlit-bentoml/

# train sklearn baseline model (RandomForestRegressor)
$ mlflow run . -e baseline --env-manager local

# train keras naive model (MLP)
$ mlflow run . -e keras_naive --env-manager local

# train keras conv2d model (Conv2D)
$ mlflow run . -e keras_conv2d --env-manager local
```
Note about flag options
- `-e`: specify the entrypoint
- `--env-manager`: use local environments without creating a conda virtual environment


## Create BentoServer




## References
- [open-source-ml-project-with-dagshub-improve-pet-adoption-with-machine-learning-1]
- [Complete Guide to Experiment Tracking With MLflow and DagsHub]
- [the-easiest-way-to-deploy-your-ml-dl-models-in-2022-streamlit-bentoml-dagshub]
- [Data version control with Python and DVC]
- [PetFinder.my - Pawpularity Contest]
- [BexTuychiev/pet_pawpularity]


[DagsHub]: https://dagshub.com/docs/index.html
[DVC]: https://dvc.org/
[MLflow]: https://www.mlflow.org/
[BentoML]: https://docs.bentoml.org/en/latest/
[Streamlit]: https://streamlit.io/
[Heroku]: https://devcenter.heroku.com/
[Data version control with Python and DVC]: https://realpython.com/python-data-version-control/
[open-source-ml-project-with-dagshub-improve-pet-adoption-with-machine-learning-1]: https://towardsdatascience.com/open-source-ml-project-with-dagshub-improve-pet-adoption-with-machine-learning-1-e9403f8f7711
[the-easiest-way-to-deploy-your-ml-dl-models-in-2022-streamlit-bentoml-dagshub]: https://towardsdatascience.com/the-easiest-way-to-deploy-your-ml-dl-models-in-2022-streamlit-bentoml-dagshub-ccf29c901dac
[Complete Guide to Experiment Tracking With MLflow and DagsHub]: https://towardsdatascience.com/complete-guide-to-experiment-tracking-with-mlflow-and-dagshub-a0439479e0b9
[PetFinder.my - Pawpularity Contest]: https://www.kaggle.com/competitions/petfinder-pawpularity-score/data
[pre-built bentoml docker image]: https://github.com/youjin2/mlops/tree/main/bentoml/docker
[examples/streamlit-bentoml/requirements.txt]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/streamlit-bentoml/requirements.txt
[BexTuychiev/pet_pawpularity]: https://github.com/BexTuychiev/pet_pawpularity
