import os

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D
from tensorflow.keras import Model

import bentoml


def load_dataset(verbose=True):
    mnist = tf.keras.datasets.mnist
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    if verbose:
        print(f"X train shape: {X_train.shape}")
        print(f"y train shape: {y_train.shape}")

        print(f"X test shape: {X_test.shape}")
        print(f"y test shape: {y_test.shape}")

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


def main():

    # load dataset
    (X_train, y_train), (X_valid, y_valid), (X_test, y_test) = load_dataset()

    # build and train the model
    model = build_model()
    model.fit(
        X_train,
        y_train,
        batch_size=64,
        epochs=10,
        validation_data=(X_valid, y_valid),
    )

    # calculate accuracies
    pred_train = tf.argmax(model.predict(X_train), axis=1)
    pred_valid = tf.argmax(model.predict(X_valid), axis=1)
    pred_test = tf.argmax(model.predict(X_test), axis=1)
    print(f"train accuracy (%): {tf.reduce_mean(tf.where(y_train == pred_train, 1., 0.))*100:0.4f}")
    print(f"valid accuracy (%): {tf.reduce_mean(tf.where(y_valid == pred_valid, 1., 0.))*100:0.4f}")
    print(f"test accuracy (%): {tf.reduce_mean(tf.where(y_test == pred_test, 1., 0.))*100:0.4f}")

    # save the model with bento save
    bentoml.tensorflow.save_model(
        "tf_custom_runner",
        model,
        signatures={"__call__": {"batchable": True, "batch_dim": 0}},
    )


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    main()
