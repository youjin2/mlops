import base64

import tensorflow as tf
import bentoml
from bentoml.io import Text, NumpyNdarray


conv2d_model = bentoml.mlflow.get("keras-conv2d-model:latest")
conv2d_runner = conv2d_model.to_runner()
svc = bentoml.Service(
    name="pawpularity-conv2d-service",
    runners=[conv2d_runner],
)


@svc.api(input=Text(), output=NumpyNdarray())
async def predict_pawpularity_score(buffer):
    width, height = (224, 224)

    # print("====="*20)
    # print(buffer)
    # print("====="*20)
    buffer = base64.b64decode(buffer)
    image = tf.image.decode_jpeg(buffer)
    resized = tf.image.resize(
        image,
        size=(width, height),
        method="bilinear",
        preserve_aspect_ratio=False,
    )
    resized /= 255.
    inputs = tf.reshape(tf.cast(resized, "float32"), (1, width, height, 3))
    scores = await conv2d_runner.async_run({
        "input_1": inputs
    })["dense_1"]

    return scores
