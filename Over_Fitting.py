import tensorflow as tf
from tensorflow import keras
import json
import numpy as np
from sklearn.model_selection import train_test_split

DATASET_PATH = "data.json"

def load_data(dataset_path):
    with open(dataset_path, "r") as fp:
        data = json.load(fp)

    # convert lists into numpy arrays
    inputs = np.array(data["mfcc"])
    targets = np.array(data["labels"])

    return inputs, targets

if __name__ == "__main__":

    # load data
    inputs, targets = load_data(DATASET_PATH)

    # split data into training and test sets
    inputs_train, inputs_test, targets_train, targets_test = train_test_split(inputs, 
                                                                              targets, 
                                                                              test_size=0.3)

    # build the network architecture
    model = tf.keras.Sequential([
        # input layer
        tf.keras.layers.Flatten(input_shape=(inputs.shape[1], inputs.shape[2])),

        # first hidden layer
        tf.keras.layers.Dense(512, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
        tf.keras.layers.Dropout(0.3),

        # second hidden layer
        tf.keras.layers.Dense(256, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
        tf.keras.layers.Dropout(0.3),

        # third hidden layer
        tf.keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
        tf.keras.layers.Dropout(0.3),

        # output layer
        tf.keras.layers.Dense(10, activation="softmax")
                                 ])

    # compile network
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer,
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"]
    )

    model.summary()

    # train network
    model.fit(inputs_train, targets_train, 
              validation_data=(inputs_test, targets_test),
              epochs=50,
              batch_size=32)
        