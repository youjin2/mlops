## Goal
Demonstrate how to use pretrained YOLOv5 model from Torch hub, and use it to build a prediction service in BentoML.


## Requirements
```bash
# install pytorch & opencv dependencies
$ apt-get install ffmpeg libsm6 libxext6  -y
$ pip install -r requirements.txt

# or
$ ./install.sh
```


## BentoML Serve
```bash
$ curl -X 'POST' 'http://localhost:12000/invocation' -H 'accept: image/jpeg' -H 'Content-Type: image/jpeg' --data-binary '@data/bus.jpg'
$ curl -X 'POST' 'http://localhost:12000/render' -H 'accept: image/jpeg' -H 'Content-Type: image/jpeg' --data-binary '@data/bus.jpg' --output './output/bus.jpeg'
```


## Containerize


## References
- [bentoml/examples/custom_runner/torch_hub_yolov5]


[bentoml/examples/custom_runner/torch_hub_yolov5]: https://github.com/bentoml/BentoML/tree/main/examples/custom_runner/torch_hub_yolov5
