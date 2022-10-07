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
    input=NumpyNdarray(dtype="float32", enforce_dtype=True),
    output=NumpyNdarray(dtype="int64"),
)
def predict(inp):
    return 1

# @svc.api(
#     input=NumpyNdarray(dtype="float32", enforce_dtype=True),
#     output=NumpyNdarray(dtype="int64"),
# )
# async def predict_ndarray(
#     inp: "np.ndarray[t.Any, np.dtype[t.Any]]",
# ) -> "np.ndarray[t.Any, np.dtype[t.Any]]":
#     assert inp.shape == (28, 28)

#     # extra channel dimension
#     inp = np.expand_dims(inp, 2)
#     output_tensor = await mnist_runner.async_run(inp)
#     return output_tensor.numpy()


# @svc.api(
#     input=Image(),
#     output=NumpyNdarray(dtype="int64")
# )
# async def predict_image(f: PILImage) -> "np.ndarray[t.Any, np.dtype[t.Any]]":
#     assert isinstance(f, PILImage)
#     arr = np.array(f)/255.0
#     assert arr.shape == (28, 28)

#     # extra channel dimension
#     arr = np.expand_dims(arr, (0, 3)).astype("float32")
#     output_tensor = await mnist_runner.async_run(arr)
#     return output_tensor.numpy()
