## Goal
In this example, we will train and deploy the `Keras image regression model` to predict the cutiness score of cats and dogs using `Pet Pawpularity dataset` on Kaggle.  
Also, we will cover various MLOps & data version control services descibed below to manage the machine learning pipeline and finally we will use `streamlit` & `bentoml` to interact with the developed model on web UI
- [DagsHub]
- [DVC]
- [MLflow]
- [BentoML]
- [Streamlit]
- [Heroku]


## Setup Dependencies
### Python environment
```bash
$ cd ./bentoml/
$ docker-compose up -d

$ docker exec -it bentoml-serving /bin/bash
$ cd examples/streamlit-bentoml/
```

### DagsHub & DVC
First, create your dagshub repository. (e.g. `https://dagshub.com/{your_dagshub_username}/petfinder`)  
Note that it is like github for data scienists and machine learning engineers.  
After creating remote respository on dagshub, clone the repository on your local environment.
```bash
$ cd ./bentoml/examples/
$ git clone https://dagshub.com/{your_dagshub_username}/petfinder.git ./petfinder/
```

Once you, you completed to setup python environment described here, you can run `dvc` on command line interface.

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
$ git commit -m "ENH: init DVC"
$ git push origin main


# add data for dvc version control
$ dvc add data/
$ git add data.dvc .gitignore
$ git commit -m "ENH: dvc add data for version control"

# push dataset to dagshub storage
$ dvc push -r origin
$ git push origin main
```

### Git Submodule
```bash
$ cd examples/streamlit-bentoml/
$ git commit -m "ENH: add dagshub petfinder submodule"
$ git push origin main
```


## 
Download Dataset





## References
- [open-source-ml-project-with-dagshub-improve-pet-adoption-with-machine-learning-1]
- [Complete Guide to Experiment Tracking With MLflow and DagsHub]
- [the-easiest-way-to-deploy-your-ml-dl-models-in-2022-streamlit-bentoml-dagshub]
- [Data version control with Python and DVC]
- [PetFinder.my - Pawpularity Contest]


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
