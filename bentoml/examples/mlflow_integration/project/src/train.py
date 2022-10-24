import os

import mlflow

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D
from tensorflow.keras import Model


def load_dataset():
    mnist = tf.keras.datasets.mnist
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # preprocess input images
    X_train = X_train.reshape(60000, 28, 28, 1).astype("float32") / 255
    X_test = X_test.reshape(10000, 28, 28, 1).astype("float32") / 255

    # Reserve 10,000 samples for validation
    X_valid = X_train[-10000:]
    y_valid = y_train[-10000:]

    X_train = X_train[:-10000]
    y_train = y_train[:-10000]

    return (X_train, y_train), (X_valid, y_valid), (X_test, y_test)


def build_model():
    # Create an instance of the model
    inputs = Input(shape=(28, 28, 1))
    x = inputs
    x = Conv2D(32, 3, activation="relu")(x)
    x = Flatten()(x)
    x = Dense(128, activation="relu")(x)
    outputs = Dense(10, activation="sigmoid")(x)

    model = Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        # Loss function to minimize
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        # List of metrics to monitor
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    return model


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # available >= tensorflow==2.8.x
    # related issue: https://github.com/tensorflow/tensorflow/issues/54286
    # mlflow.tensorflow.autolog()
    mlflow.keras.autolog()
    with mlflow.start_run(run_name="train_model"):
        # load dataset
        (X_train, y_train), (X_valid, y_valid), (X_test, y_test) = load_dataset()

        # log dataset informations
        mlflow.log_dict(
            {
                "X_train": f"{X_train.shape}",
                "y_train ": f"{y_train.shape}",
                "X_test": f"{X_test.shape}",
                "y_test": f"{y_test.shape}",
            },
            "data_shape.json"
        )

        # build and train the model
        model = build_model()
        model.fit(
            X_train,
            y_train,
            batch_size=128,
            epochs=2,
            validation_data=(X_valid, y_valid),
        )
        tf.saved_model.save(model, "./tmp_model/")

        # calculate accuracies
        pred_train = tf.argmax(model.predict(X_train), axis=1)
        pred_valid = tf.argmax(model.predict(X_valid), axis=1)
        pred_test = tf.argmax(model.predict(X_test), axis=1)
        mlflow.log_dict(
            {
                "train_accuracy (%)": f"{tf.reduce_mean(tf.where(y_train == pred_train, 1., 0.))*100:0.4f}",
                "valid_accuracy (%)": f"{tf.reduce_mean(tf.where(y_valid == pred_valid, 1., 0.))*100:0.4f}",
                "test_accuracy (%)": f"{tf.reduce_mean(tf.where(y_test == pred_test, 1., 0.))*100:0.4f}",
            },
            "train_result.json"
        )

        # log model
        mlflow.tensorflow.log_model(
            tf_saved_model_dir="./tmp_model/",
            # tf.saved_model.SERVING
            tf_meta_graph_tags=["serve"],
            # tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY
            tf_signature_def_key="serving_default",
            artifact_path="tf-mnist-demo",
        )
