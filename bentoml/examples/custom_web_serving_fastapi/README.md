## Goal


## Install dependencies
You may install `fastapi`
```bash
$ cd examples/custom_web_serving_fastapi

# install additional dependencies on your container
$ pip install -r requirements.txt
```


## Train & save the model
```bash
$ cd examples/custom_web_serving_fastapi

# after runnning the training script, check out that the model saved at "${BENTOML_HOME}/models/iris_clf_with_feature_names/" successfully.
$ python train.py
```


## BentoML Serve
```bash

# "/predict_bentoml" endpoint:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": 7.2, "sepal_width": 3.2, "petal_len": 5.2, "petal_width": 2.2}' http://127.0.0.1:12000/predict_bentoml

# "/predict_fastapi" endpoint:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": 6.2, "sepal_width": 3.2, "petal_len": 5.2, "petal_width": 2.2}' http://127.0.0.1:12000/predict_fastapi

# "/predict_fastapi_async" endpoint:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": 6.2, "sepal_width": 3.2, "petal_len": 5.2, "petal_width": 2.2}' http://127.0.0.1:12000/predict_fastapi_async

# "/metadata" endpoint:
$ curl http://127.0.0.1:12000/metadata
```



## References
- [bentoml/examples/custom_web_serving/fastapi_example]


[bentoml/examples/custom_web_serving/fastapi_example]: https://github.com/bentoml/BentoML/tree/main/examples/custom_web_serving/fastapi_example
