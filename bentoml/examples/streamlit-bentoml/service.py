import base64

import numpy as np
import tensorflow as tf
import bentoml
from bentoml.io import Image, Text, NumpyNdarray


conv2d_model = bentoml.mlflow.get("keras-conv2d-model:latest")
conv2d_runner = conv2d_model.to_runner()
svc = bentoml.Service(
    name="pawpularity-conv2d-service",
    runners=[conv2d_runner],
)


def preprocess_text(image_buffer: str):
    """preprocess_text.
    get text image buffer and convert it to 3d-image tensor.
    """
    image_buffer = base64.b64decode(image_buffer)
    image = tf.image.decode_jpeg(image_buffer)

    return image


def preprocees_image(image: tf.Tensor):
    """preprocees_image.
    """
    width, height = (224, 224)

    resized = tf.image.resize(
        image,
        size=(width, height),
        method="bilinear",
        preserve_aspect_ratio=False,
    )
    resized /= 255.
    inputs = tf.reshape(tf.cast(resized, "float32"), (1, width, height, 3))

    return inputs


@svc.api(input=Text(), output=NumpyNdarray())
def predict_text(image_buffer: str):
    image = preprocess_text(image_buffer)
    inputs = preprocees_image(image)
    scores = conv2d_runner.run({"input_1": inputs})["dense_1"]

    return scores


@svc.api(input=Image(), output=NumpyNdarray())
def predict_image(image: tf.Tensor):
    image = np.array(image)
    inputs = preprocees_image(image)
    scores = conv2d_runner.run({"input_1": inputs})["dense_1"]

    return scores


# @svc.api(input=Text(), output=NumpyNdarray())
# async def predict_pawpularity_score(buffer):
#     # TODO: how to use async api for tensorflow==2.4
#     inputs = preprocess(buffer)
#     scores = await conv2d_runner.async_run({"input_1": inputs})

#     return scores
