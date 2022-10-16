import bentoml
from bentoml.io import Image, NumpyNdarray
import numpy as np


mnist_model = bentoml.tensorflow.get("tf_custom_runner:latest")
mnist_runnable = mnist_model.to_runnable()


class CustomMnistRunnable(mnist_runnable):
    def __init__(self):
        super().__init__()
        import tensorflow

        print("Running on device:", tensorflow.config.list_physical_devices())
        print("Running on tensorflow version:", tensorflow.__version__)

    @bentoml.Runnable.method(batchable=True, batch_dim=0)
    def __call__(self, input_array):
        output = super().__call__(input_array)
        return np.argmax(output, axis=1)


mnist_runner = bentoml.Runner(
    CustomMnistRunnable,
    method_configs={"__call__": {"max_batch_size": 50, "max_latency_ms": 600}},
)
svc = bentoml.Service(
    "tf_custom_runner_demo",
    runners=[mnist_runner],
    models=[mnist_model],
)


@svc.api(input=Image(), output=NumpyNdarray())
async def predict(input_img):
    # passing an array having a different dtype from model signature options may raise error below.
    # "Could not find matching function to call loaded from the SavedModel"
    input_arr = np.array(input_img).reshape([1, 28, 28, 1]).astype("float32")
    batch_ret = await mnist_runner.async_run(input_arr)
    return batch_ret[0]
