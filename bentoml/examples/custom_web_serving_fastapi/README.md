## Goal
Customize the serving API with `fastapi` and use `pydantic` validation to check the data type of given parameters are passed appropriately.  
You can see that how `fastapi` supports the automatic validation and type conversion using `pydantic` classes and how `bentoml` automatically converts the input data type required to passed to the model.


## Install dependencies
You may have to install additional dependencies.
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

# check the saved models
$ bentoml models list

outputs:
 Tag                                           Module                   Size       Creation Time
 iris_clf_with_feature_names:bv6dn4cnicezyasc  bentoml.sklearn          6.34 KiB   2022-10-16 19:48:21
```


## BentoML Serve
```bash
$ cd examples/custom_web_serving_fastapi

# launch api server
$ bentoml serve service:svc --host 0.0.0.0 --port 3000 --reload

# "/predict_bentoml" endpoint:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": 7.2, "sepal_width": 3.2, "petal_len": 5.2, "petal_width": 2.2}' http://127.0.0.1:12000/predict_bentoml

# "/predict_bentoml" endpoint with mis-specified data type:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": "7.2", "sepal_width": "3.2", "petal_len": "5.2", "petal_width": "2.2"}' http://127.0.0.1:12000/predict_bentoml

# "/predict_bentoml_wo_pydantic" endpoint (type conversion is required):
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": "7.2", "sepal_width": "3.2", "petal_len": "5.2", "petal_width": "2.2"}' http://127.0.0.1:12000/predict_bentoml_wo_pydantic

# "/predict_fastapi" endpoint:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": 6.2, "sepal_width": 3.2, "petal_len": 5.2, "petal_width": 2.2}' http://127.0.0.1:12000/predict_fastapi

# "/predict_fastapi" endpoint with mis-specified data type:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": "7.2", "sepal_width": "3.2", "petal_len": "5.2", "petal_width": "2.2"}' http://127.0.0.1:12000/predict_fastapi

# "/predict_fastapi_async" endpoint:
$ curl -X POST -H "content-type: application/json" --data '{"sepal_len": 6.2, "sepal_width": 3.2, "petal_len": 5.2, "petal_width": 2.2}' http://127.0.0.1:12000/predict_fastapi_async

# "/metadata" endpoint:
$ curl http://127.0.0.1:12000/metadata
```


## Build bento & dockerize the API service
```bash
$ cd examples/custom_web_serving_fastapi

# build bentos
$ bentoml build

# build docker container
$ export BENTOML_HOME=../../bentoml/models
$ bentoml containerize iris_fastapi_demo:latest
$ docker images

output:
REPOSITORY                   TAG                IMAGE ID       CREATED          SIZE
iris_fastapi_demo            mzi6ctso4scdaasc   e11433965248   20 seconds ago   847MB

# launch api server
$ docker run --rm -p 12000:3000 iris_fastapi_demo:mzi6ctso4scdaasc serve --production
```



## References
- [bentoml/examples/custom_web_serving/fastapi_example]
- [bentoml/examples/pydantic_validation]


[bentoml/examples/custom_web_serving/fastapi_example]: https://github.com/bentoml/BentoML/tree/main/examples/custom_web_serving/fastapi_example
[bentoml/examples/pydantic_validation]: https://github.com/bentoml/BentoML/tree/main/examples/pydantic_validation
