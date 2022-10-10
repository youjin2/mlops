## Introduction
This tutorial will cover the [Tutorial: Intro to BentoML], which includes training, saving and serving a ML model.  
For model training & saving, see [01_introduction_to_bentoml.ipynb] for more details.  
By running command below in the container, you can check out & manage the saved models.  
```bash
# pre-requisite: train/save model by running "01_introduction_to_bentoml.ipynb"
$ docker exec -it bentoml-serving /bin/bash
$ cd /opt/project/
$ bentoml models list
 Tag                        Module           Size      Creation Time
 iris_clf:iuf2xbcbl2pweasc  bentoml.sklearn  5.98 KiB  2022-10-01 07:54:25
```

Now, run the BentoML server for our new service in development mode.  
```bash
# run command below in the docker container and open "http://127.0.0.1:12000/" in your browser
$ cd bentoml/examples/tutorial
$ bentoml serve tutorial_service:svc --reload --host 0.0.0.0 --port 3000

# request prediction in your local machine
$ curl -X POST \
   -H "content-type: application/json" \
   --data "[[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [7.0, 3.2, 4.7, 1.4], [6.8, 3.2, 5.9, 2.3]]" \
   http://127.0.0.1:12000/classify
```

Build the model and service into a bento, self-contained archive that contains all the source code, model files and dependency specifications required to run the service.
```bash
# create bentofile.yaml first, and run command below in CLI
$ cd bentoml/examples/tutorial
$ export BENTOML_HOME=../../bentoml/ && bentoml build

$ cd bentoml/
$ tree bentoml/bentos/iris_classifier

# outputs:
bentoml/bentos/iris_classifier
├── latest
└── pbwm46sdcos4cmoq
    ├── apis
    │   └── openapi.yaml
    ├── bento.yaml
    ├── env
    │   ├── docker
    │   │   ├── Dockerfile
    │   │   └── entrypoint.sh
    │   └── python
    │       ├── install.sh
    │       ├── requirements.lock.txt
    │       ├── requirements.txt
    │       └── version.txt
    ├── models
    │   └── iris_clf
    │       ├── latest
    │       └── rlakk2cdccseyasc
    │           ├── model.yaml
    │           └── saved_model.pkl
    ├── README.md
    └── src
        ├── __init__.py
        └── service.py

# serving in production
$ bentoml serve iris_classifier:latest --production
```

A docker image can be automatically generated from a Bento for production deployment.  
```bash
# run command below in your local macihne (host)
$ bentoml containerize iris_classifier:latest

# check out the result for docker build
$ docker images

# output: 
REPOSITORY                   TAG                IMAGE ID       CREATED          SIZE
iris_classifier              pbwm46sdcos4cmoq   7a140b976a71   24 seconds ago   834MB

# run the docker image and start BentoServer (tag may differ for other environment)
$ docker run -it --rm -p 12000:3000 iris_classifier:pbwm46sdcos4cmoq serve --production

# request prediction in your local machine (host)
$ curl -X POST \
   -H "content-type: application/json" \
   --data "[[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [7.0, 3.2, 4.7, 1.4], [6.8, 3.2, 5.9, 2.3]]" \
   http://127.0.0.1:12000/classify
```


## Practical examples
First, train mnist classifier with tensorflow and save the model with BentoML. (see [02_tensorflow_mnist_pipeline.ipynb])  
In that notebook, you can also check that the model is loaded well and prediction API has no problem in native Python shell.

After training and saving the model finished, create ML service code `service.py` file.  
See [examples/tensorflow_serving/service.py] for detailed code examples.  
Now launch the API server by running command below on your docker container.  
(`bentofile.yaml` is not required at this stage)
```bash
$ cd /examples/tensorflow_serving/

# NOTE: reload automatically api sever when code changes detected
$ bentoml serve service:svc --reload
```

On your local machine, you can get the prediction result by 
```bash
# use "predict_image" API
$ curl -H "Content-Type: multipart/form-data" -F'fileobj=@samples/0.png;type=image/png' http://127.0.0.1:12000/predict_image
```
or, by using the native Python shell.
```python
import requests

from PIL import Image
import numpy as np


img = Image.open("./samples/0.png")
arr = np.array(img)

# use "predict_ndarray" API
response = requests.post(
    # for running request on local machine
    "http://127.0.0.1:12000/predict_ndarray",
    # for running request on container
    # "http://127.0.0.1:3000/predict_ndarray",
    json=arr.tolist()
)

print(response.status_code)
print(response.content)
```

TODO: benchmark with `locust`
```bash
$ locust --headless -u 100 -r 1000 --run-time 10m --host http://127.0.0.1:3000
```

Now, write `bentofile.yaml` to build Bento for deployment. (see `./examples/tensorflow_serving/bentofile.yaml`)  
Run commands below (on host or container) and check that `${BENTOML_HOME}/tensorflow_mnist_demo` created.
```bash
$ cd ./examples/tensorflow_serving/
$ bentoml build

$ tree ${BENTOML_HOME}

# outputs:
bentos/
└── tensorflow_mnist_demo
    ├── 3nceqwchcoi6kasc
    │   ├── apis
    │   ├── env
    │   │   ├── docker
    │   │   └── python
    │   ├── models
    │   │   └── tensorflow_mnist
    │   │       └── q7dqa6cg2cyyiasc
    │   │           ├── assets
    │   │           └── variables
    │   └── src
```

After building the bento finished, run command below on container to serve the production model.  
```
$ bentoml serve tensorflow_mnist_demo:latest --production
```

You can also containerize the api server with:
```bash
# project home (not ${BENTOML_HOME})
$ cd bentoml/
$ bentoml containerize tensorflow_mnist_demo:latest

# if "BENTOML_HOME" environment variable not identified yet, you may see below error message.
# Error: [bentoml-cli] `containerize` failed: no Bentos with name 'tensorflow_mnist_demo' exist in BentoML store <osfs '/home/youjin2/bentoml/bentos'>
# then, set environment variable and run `bento containerize` again.
$ export BENTOML_HOME=./bentoml/

# launch containerized api server
$ docker run --rm -p 12000:3000 tensorflow_mnist_demo:3nceqwchcoi6kasc serve --production
```




## Custom Python model & Model runner





## References
- [Tutorial: Intro to BentoML]
- [BentoML examples: tensorflow2 keras]
- [Bentoml basic tutorial (Korean)]



[Tutorial: Intro to BentoML]: https://docs.bentoml.org/en/latest/tutorial.html
[1.0.0 Migration Guide]: https://docs.bentoml.org/en/latest/guides/migration.html
[Bentoml basic tutorial (Korean)]: https://zzsza.github.io/mlops/2021/04/18/bentoml-basic/
[01_introduction_to_bentoml.ipynb]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/01_introduction_to_bentoml.ipynb
[02_tensorflow_mnist_pipeline.ipynb]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/02_tensorflow_mnist_pipeline.ipynb
[examples/tensorflow_serving/service.py]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/tensorflow_serving/service.py
[BentoML examples: tensorflow2 keras]: https://github.com/bentoml/BentoML/tree/main/examples/tensorflow2_keras
[tmp]: https://towardsdatascience.com/bentoml-create-an-ml-powered-prediction-service-in-minutes-23d135d6ca76

