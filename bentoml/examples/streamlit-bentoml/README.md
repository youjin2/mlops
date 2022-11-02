## Goal
In this example, we will train and deploy the `Keras image regression model` to predict the cutiness score of cats and dogs using `Pet Pawpularity dataset` on Kaggle.  
Also, we will cover various MLOps & data version control services descibed below to manage the machine learning pipeline and finally we will use `streamlit` & `bentoml` to interact with the developed model on web UI
- [DagsHub]
- [DVC]
- [MLflow]
- [BentoML]
- [Streamlit]
- [Heroku]


## Setup dependencies
```bash
$ cd ./bentoml/
$ docker-compose up -d

$ docker exec -it bentoml-serving /bin/bash
$ cd examples/streamlit-bentoml/
```


## 



## References
- [open-source-ml-project-with-dagshub-improve-pet-adoption-with-machine-learning-1]
- [Complete Guide to Experiment Tracking With MLflow and DagsHub]
- [the-easiest-way-to-deploy-your-ml-dl-models-in-2022-streamlit-bentoml-dagshub]
- [Data version control with Python and DVC]


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
