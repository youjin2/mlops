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

Test prediction request.
<a name="api-request"></a>
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

**[NOTE]**  
Currently, requesting API for `pd.DataFrame` output like below fails because of mis-matching type error.  
```python
@svc.api(input=Image(), output=PandasDataFrame())
async def invocation(input_img):
    batch_ret = await yolo_v5_runner.inference.async_run([input_img])
    return batch_ret[0]
```
I think [bentoml/_internal/io_descriptors/pandas.py#L513] should be fixed like below.  
```python
if not LazyType["ext.PandasDataFrame"]("pandas.DataFrame").isinstance(dataframe):
```
But have no idea why `LazyLoader` does not overwrite `import pandas as pd` with bentoml's `ext.PdDataFrame` type.


## Containerize
Build and launch the containerized API server with:
```bash
$ ./examples/custom_runner/

# build bento (local or container)
$ bentoml build

# build container image (local)
$ export BENTOML_HOME=../../bentoml/
$ bentoml containerize yolo_v5_demo:latest

# check image built status
$ docker images

output: 
REPOSITORY                   TAG                IMAGE ID       CREATED              SIZE
yolo_v5_demo                 ebhb2dslasisiasc   0cc96e8dd150   About a minute ago   2.8GB

# serving with docker conatiner
$ docker run --rm -p 12000:3000 yolo_v5_demo:ebhb2dslasisiasc serve --production
```
After containerized API server created, run [this](#api-request) to get a prediction response.


## References
- [bentoml/examples/custom_runner/torch_hub_yolov5]
- [bentoml/_internal/io_descriptors/pandas.py#L513]
- [BentoML/issues/2219]


[bentoml/examples/custom_runner/torch_hub_yolov5]: https://github.com/bentoml/BentoML/tree/main/examples/custom_runner/torch_hub_yolov5
[bentoml/_internal/io_descriptors/pandas.py#L513]: https://github.com/bentoml/BentoML/blob/main/src/bentoml/_internal/io_descriptors/pandas.py#L513
[BentoML/issues/2219]: https://github.com/bentoml/BentoML/issues/2219
[examples/custom_runner/torch_hub_test.ipynb]: https://github.com/youjin2/mlops/blob/main/bentoml/examples/custom_runner/torch_hub_test.ipynb
[BentoML/pull/2220]: https://github.com/bentoml/BentoML/pull/2220
