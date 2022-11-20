## Goal
In this example, we will train and deploy `image regression model` to predict the cutiness score of cats and dogs using `Pet Pawpularity dataset` on Kaggle.  
Also, we will cover various MLOps & data version control services listed below to manage the machine learning pipeline and finally we will use `streamlit` & `bentoml` to serve the developed model on web UI.
- [DagsHub]
- [DVC]
- [MLflow]
- [BentoML]
- [Streamlit]
- [Heroku]


## Setup Dependencies
### Python environment
We will use [pre-built bentoml docker image] as a base python development environment for this example.  
Additional dependencies (`mlflow`, `dagshub`, `dvc`, ...) are specified in [examples/streamlit-bentoml/requirements.txt] and they are automatically installed while running `docker-compose up`.
```bash
$ cd examples/streamlit-bentoml/
$ docker-compose up -d
$ docker exec -it bentoml-serving /bin/bash
```

### DagsHub & DVC
Dagshub is a github-like open source platform for data scientist and machine learning engineers to versioning their data, models, experiments and codes.  
We will cover a brief introduction here for doing version control about our `Pawpularity` dataset using dagshub.

First, create your dagshub repository. (e.g. `https://dagshub.com/{your_dagshub_username}/petfinder`)  
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

# download dataset from my repo (I already stored the dataset to my remote repository)
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
You can import the model saved at `MLflow tracking server` by running commands below.  
(Note that bentoml supports the API importing MLflow model to BentoML model store)
```bash
$ cd examples/streamlit-bentoml/

# set your mlflow tracking server credentials
$ export MLFLOW_TRACKING_USERNAME={your_dagshub_username}
$ export MLFLOW_TRACKING_PASSWORD={your_dagshub_password}

# save bento model from mlflow tracking server
$ python -m src.save_bento_model

# check out the bento saved model
$ bentoml models list

# expected output:
 Tag                                  Module          Size       Creation Time
 keras-conv2d-model:jjvzu5tdkcf3yasc  bentoml.mlflow  54.78 MiB  2022-11-13 12:40:01
```

After saving the bento model, you can run API server on the docker container with:
```bash
$ cd examples/streamlit-bentoml/

# run api server
$ bentoml serve service.py:svc --host 0.0.0.0 --port 3000 --reload
```

You can check out the API reponse on CLI with:
```bash
$ curl -X 'POST' \
  'http://localhost:12000/predict_image' \
  -H 'accept: application/json' \
  -H 'Content-Type: image/jpeg' \
  --data-binary '@petfinder/data/raw/train/0365920c849af714930d75e7727c5165.jpg'

```

or in Python with:
```python
import requests
import json
import base64


with open("petfinder/data/raw/train/0365920c849af714930d75e7727c5165.jpg", "rb") as f:
    image_buffer = f.read()

response = requests.post(
    "http://0.0.0.0:12000/predict_text",
    # "http://0.0.0.0:3000/predict_text",
    data=base64.b64encode(image_buffer),
    headers={"content-type": "text/plain"},
)
print(json.loads(response.text))
```


## Build the Bento
To build a bento to deploy our API server, first write a `bentoml.yaml` file which specifies the service and requirements to launch an API server.  
Note that we bind bento service as `svc = bentoml.Service(...)`.
```yaml
service: "service.py:svc"
include:
 - "service.py"
python:
  packages:
   - scikit-learn==1.1.2
   - tensorflow==2.5.0
   - numpy~=1.19.2
   - Pillow==9.2.0
   - bentoml==1.28.0
```

And then, build the bento by running command below in your docker container.
```bash
$ cd examples/streamlit-bentoml/

# build the bento
$ bentoml build

# check out the bento created
$ bentoml list
 Tag                                          Size       Creation Time        Path
 pawpularity-conv2d-service:l7e46fthj6cgqasc 54.81 MiB  2022-11-18 13:25:17  /bentoml/bentos/pawpularity-conv2d-service/nyjnowdhisbhcasc
```

You can test containerized API server by running command below on your local machine.
```bash
$ cd examples/streamlit-bentoml/

# set "BENTOML_HOME" environment variable
$ export BENTOML_HOME=`pwd`/bentoml/

# build docker container (bentoml installation required)
$ bentoml containerize pawpularity-conv2d-service:latest

# check out docker images
$ docker images

expected output:
REPOSITORY                   TAG                IMAGE ID       CREATED              SIZE
pawpularity-conv2d-service   l7e46fthj6cgqasc   1b2fa2a5c622   About a minute ago   2.13GB

# run dockerized API server
$ docker run --rm -p 12000:3000 pawpularity-conv2d-service:l7e46fthj6cgqasc serve --production
```



## Deploy to Heroku
### Setup Heroku CLI
`Heroku` is a cloud-based SaaS platform managed by Salesforce that enables developers to build, run and operate the applications.  
Here we are going to use Heroku to deploy our `streamlit web UI` service.

First, [create a Heroku account] and [download the Heroku CLI] to create and manage the apps.  
Just run below to install the Heroku CLI.
```bash
$ curl https://cli-assets.heroku.com/install.sh | sh
```

You can login to Heroku CLI by opening web brower and get the credentials automatically:
```bash
$ heroku login
heroku: Press any key to open up the browser to login or q to exit
 ›   Warning: If browser does not open, visit
 ›   https://cli-auth.heroku.com/auth/browser/***
heroku: Waiting for login...
Logging in... done
Logged in as my@email.com
```

If you want to stay in the CLI to enter your crendentials, then run:
```bash
$ heroku login -i
Email [my@email.com]: my@email.com
Password: ************
Logged in as my@email.com
```

### Deploy the Bento and Launch API service
First, we need to create a heroku app for our API service.
```bash
# login to container registry
$ heroku container:login

# create an app name "youjin2-pet-pawpularity"
# (you may use any other your own app name)
$ heroku create youjin2-pet-pawpularity
```

After finishing creaeting an app, deploy our containerized API servce.
```bash
$ cd examples/streamlit-bentoml

# change directory to {BENTOML_HOME}/{OUR_LATEST_SERVICE}
$ bentoml/bentos/pawpularity-conv2d-service/l7e46fthj6cgqasc/

# change directory which docker file saved
$ cd env/docker

# push docker conatiner to heroku
$ heroku container:push web --app youjin2-pet-pawpularity --context-path=../../

# if you get an error message like below, you need to enable docker BuildKit
# reference: https://docs.docker.com/build/buildkit/#getting-started
the --mount option requires BuildKit. Refer to https://docs.docker.com/go/buildkit/ to learn how to build images with BuildKit enabled
 ▸    Error: docker build exited with Error: 1

# option 1. To enable the docker BuildKit by default, please add below to "/etc/docker/daemon.json"
{
  "features": {
    "buildkit" : true
  }
}

# option 2. You can set an environment variable
# (I couldn't solve the problem by using this option)
$ DOCKER_BUILDKIT=1

# now restart the docker container and push docker container to heroku again
$ sudo service docker stop
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
$ heroku container:push web --app youjin2-pet-pawpularity --context-path=../../
```

Finally, release the app with the command below:
```bash
$ heroku container:release web --app youjin2-pet-pawpularity

# open https://youjin2-pet-pawpularity.herokuapp.com/ on your browser
```



## Streamlit web UI





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
[create a Heroku account]: https://signup.heroku.com/
[download the Heroku CLI]: https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli
