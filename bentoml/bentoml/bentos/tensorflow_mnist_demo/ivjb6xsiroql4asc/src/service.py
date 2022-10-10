import typing as t
import os

import numpy as np
from PIL.Image import Image as PILImage

import bentoml
from bentoml.io import Image
from bentoml.io import NumpyNdarray


os.environ["CUDA_VISIBLE_DEVICES"] = ""


mnist_runner = bentoml.tensorflow.get("tensorflow_mnist:latest").to_runner()
svc = bentoml.Service(
    name="tensorflow_mnist_demo",
    runners=[
        mnist_runner,
    ],
)


@svc.api(
    input=NumpyNdarray(dtype="uint8", enforce_dtype=True),
    output=NumpyNdarray(dtype="int64"),
)
async def predict_ndarray(
    inp: "np.ndarray[t.Any, np.dtype[t.Any]]",
) -> "np.ndarray[t.Any, np.dtype[t.Any]]":
    assert inp.shape == (28, 28)

    # extra channel dimension
    inp = inp.astype("float32")
    inp = np.expand_dims(inp, (0, 3)) / 255.
    output_arr = await mnist_runner.async_run(inp)
    pred_labels = np.argmax(output_arr, axis=1)

    return pred_labels


@svc.api(
    input=Image(),
    output=NumpyNdarray(dtype="int64")
)
async def predict_image(f: PILImage) -> "np.ndarray[t.Any, np.dtype[t.Any]]":
    assert isinstance(f, PILImage)
    arr = np.array(f)/255.0
    assert arr.shape == (28, 28)

    # extra channel dimension
    arr = np.expand_dims(arr, (0, 3)).astype("float32")
    output_arr = await mnist_runner.async_run(arr)
    pred_labels = np.argmax(output_arr, axis=1)

    return pred_labels
