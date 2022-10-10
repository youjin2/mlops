## Train & Save custom python model
Most pure python code based ML model implementation should work with `bentoml.picklable_model` out-of-the-box.
```bash
$ cd examples/custom_python_model/
$ python ./train.py
```

## BentoML Serve
```bash
$ cd examples/custom_python_model/
$ bentoml serve service.py:svc

# test api request
# on container
$ curl -X POST -H "content-type: application/json" --data "[[5.9, 3, 5.1, 1.8]]" http://127.0.0.1:3000/classify
# on local host
$ curl -X POST -H "content-type: application/json" --data "[[5.9, 3, 5.1, 1.8]]" http://127.0.0.1:12000/classify
```

## Containerize
```bash
$ cd examples/custom_python_model/

# build bento
$ bentoml build

# build docker container
$ bentoml containerize iris_classifier_lda:latest

# run containerized api server
$ docker run --rm -p 12000:3000 iris_classifier_lda:romsecsiscdqmmyx serve --production
```


## References
- [bentoml/examples/custom_python_model/lda_classifier]

[bentoml/examples/custom_python_model/lda_classifier]: https://github.com/bentoml/BentoML/tree/main/examples/custom_python_model/lda_classifier
