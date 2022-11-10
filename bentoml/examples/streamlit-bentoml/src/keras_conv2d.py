import mlflow

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    MaxPool2D,
    Flatten,
    Dense,
    Dropout,
)
from tensorflow.keras.constraints import non_neg
from tensorflow.keras.callbacks import EarlyStopping

from .utils import (
    set_mlflow_crendentials,
    get_conv2d_metadata,
    mean_squared_error,
    mean_absolute_error,
)


class ImageGenerator:
    def __init__(self):
        pass

    @staticmethod
    def read_iamge(path: str):
        buffer = tf.io.read_file(path)
        image = tf.io.decode_jpeg(buffer)
        return image

    @staticmethod
    def resize_image(image: tf.Tensor, size: tuple):
        # force image shape to be squared (aspect_ratio)
        resized = tf.image.resize(
            image,
            size=size,
            method="bilinear",
            preserve_aspect_ratio=False
        )
        resized /= 255.
        return resized

    def get_dataset(self,
                    paths: list,
                    scores: list,
                    batch_size: int = 64,
                    image_shape: tuple = (224, 224),
                    num_parallel: int = tf.data.AUTOTUNE,
                    shuffle: bool = False):

        scores = tf.reshape(scores, (-1, 1))
        dataset = tf.data.Dataset.from_tensor_slices((paths, scores))

        # shuffle for trainig phase
        if shuffle:
            buffer_size = len(paths)
            dataset = dataset.shuffle(buffer_size)

        # read & resize images
        dataset = dataset.map(
            lambda x, y: [self.read_iamge(x), tf.cast(y, "float32")],
            num_parallel_calls=num_parallel,
        )
        dataset = dataset.map(
            lambda x, y: [self.resize_image(x, image_shape), y],
            num_parallel_calls=num_parallel,
        )

        # to batch dataset
        dataset = dataset.batch(batch_size)

        return dataset


def get_keras_conv2d():
    """A function to build an instance of a Keras conv2d model."""
    inputs = Input(shape=(224, 224, 3))
    x = inputs

    x = Conv2D(filters=32, kernel_size=3, padding="same", activation="relu")(x)
    x = MaxPool2D(2)(x)

    x = Conv2D(filters=34, kernel_size=3, padding="same", activation="relu")(x)
    x = MaxPool2D(3)(x)
    x = Dropout(0.25)(x)

    x = Conv2D(filters=128, kernel_size=3, padding="same", activation="relu")(x)
    x = MaxPool2D(3)(x)
    x = Dropout(0.25)(x)

    x = Flatten()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    outputs = Dense(1, activation="linear", kernel_constraint=non_neg())(x)

    model = Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="mse",
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )

    return model


if __name__ == "__main__":
    set_mlflow_crendentials()

    # load dataset
    (X_train, y_train), (X_valid, y_valid) = get_conv2d_metadata()
    image_gen = ImageGenerator()
    train_dataset = image_gen.get_dataset(
        paths=X_train,
        scores=y_train,
        batch_size=64,
        image_shape=(224, 224),
        shuffle=True,
    )

    valid_dataset = image_gen.get_dataset(
        paths=X_valid,
        scores=y_valid,
        batch_size=64,
        image_shape=(224, 224),
        shuffle=False,
    )

    # build model
    model = get_keras_conv2d()
    es_callback = EarlyStopping(monitor="val_root_mean_squared_error", patience=5)

    # run mlflow experiment
    mlflow.set_experiment("Pawpularity Score")
    with mlflow.start_run(run_name="keras_conv2d"):
        model.fit(
            train_dataset,
            validation_data=valid_dataset,
            epochs=30,
            callbacks=[es_callback],
        )

        # create train dataset again w/o shuffling
        train_dataset = image_gen.get_dataset(
            paths=X_train,
            scores=y_train,
            batch_size=64,
            image_shape=(224, 224),
            shuffle=False,
        )
        pred_train = model.predict(train_dataset)
        pred_valid = model.predict(valid_dataset)

        print(f"Train MSE: {mean_squared_error(y_train, pred_train)}")
        print(f"Test MSE: {mean_squared_error(y_valid, pred_valid)}")

        # log metrics manually
        # current version of tensorflow does not supports the mlflow.autolog()
        mlflow.log_metric("training_mae", mean_absolute_error(y_train, pred_train))
        mlflow.log_metric("training_mse", mean_squared_error(y_train, pred_train)**2)
        mlflow.log_metric("training_rmse", mean_squared_error(y_train, pred_train))
        mlflow.log_metric("valid_mae", mean_absolute_error(y_valid, pred_valid))
        mlflow.log_metric("valid_mse", mean_squared_error(y_valid, pred_valid)**2)
        mlflow.log_metric("valid_rmse", mean_squared_error(y_valid, pred_valid))
