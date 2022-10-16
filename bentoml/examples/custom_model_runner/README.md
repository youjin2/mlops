## Goal
In this example, we reproduce the [serving mnist classfier with tensorflow] and build the custom runner by inheriting the saved bentoml runnable model.


## Train & save the model
```bash
$ cd examples/custom_model_runner/

# after runnning script finished, check out that "${BENTOML_HOME}/models/tf_custom_runner/" created
$ python train.py
```

## BentoML Server
```bash

$ curl -F 'image=@samples/0.png' http://127.0.0.1:12000/predict
```


## References
- [bentoml/examples/custom_model_runner]


[bentoml/examples/custom_model_runner]: https://github.com/bentoml/BentoML/tree/main/examples/custom_model_runner
[serving mnist classfier with tensorflow]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/tensorflow_serving/
