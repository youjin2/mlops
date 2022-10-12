## Goal
Demonstrate how to use pretrained YOLOv5 model from Torch hub, and use it to build a prediction service in BentoML.


## Requirements
If you use the container image provided by this repository, additional dependencies need to be installed like below.
```bash
# (manually) install pytorch & opencv dependencies
$ apt-get install ffmpeg libsm6 libxext6  -y
$ pip install -r requirements.txt

# or
$ ./install.sh
```

## Examples for YOLOv5
see [examples/custom_runner/torch_hub_test.ipynb]


## BentoML Serve
Serve pre-trained YOLOv5 model with `bentoml serve`.
```bash
$ ./examples/custom_runner/
$ bentoml serve service.py:svc --host 0.0.0.0 --port 3000 --reload
```

Currently, api request for `pd.DataFrame` output failed because of type mis-matching error.  
I think [bentoml/_internal/io_descriptors/pandas.py#L513] should be fixed like below.  
```python
if LazyType["ext.PdDataFrame"]("pd.DataFrame").isinstance(dataframe):
```
There's an issue report ([BentoML/issues/2219]) related to above problem, but have no idea why [BentoML/pull/2220] was merged with `if not LazyTpye ...`.

```bash
# pd.DataFrame output
$ curl -X 'POST' \
    'http://localhost:12000/invocation' \
    -H 'accept: image/jpeg' \
    -H 'Content-Type: image/jpeg' \
    --data-binary '@data/bus.jpg'

# Image output
$ curl -X 'POST' \
    'http://localhost:12000/render' \
    -H 'accept: image/jpeg' \
    -H 'Content-Type: image/jpeg' \
    --data-binary '@data/bus.jpg' \
    --output './output/bus.jpeg'
```


## Containerize


## References
- [bentoml/examples/custom_runner/torch_hub_yolov5]
- [bentoml/_internal/io_descriptors/pandas.py#L513]
- [BentoML/issues/2219]


[bentoml/examples/custom_runner/torch_hub_yolov5]: https://github.com/bentoml/BentoML/tree/main/examples/custom_runner/torch_hub_yolov5
[bentoml/_internal/io_descriptors/pandas.py#L513]: https://github.com/bentoml/BentoML/blob/main/src/bentoml/_internal/io_descriptors/pandas.py#L513
[BentoML/issues/2219]: https://github.com/bentoml/BentoML/issues/2219
[examples/custom_runner/torch_hub_test.ipynb]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/custom_runner/torch_hub_test.ipynb
[BentoML/pull/2220]: https://github.com/bentoml/BentoML/pull/2220
