import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
import Pipeline.Training_Data_Pipeline as preprocessed

#import matplotlib.pyplot as plt
y_label = "IDENTIFIER"

x_train = preprocessed.x_train
x_test  = preprocessed.x_test
y_train = preprocessed.y_train["IDENTIFIER"]
y_test  = preprocessed.y_test["IDENTIFIER"]


def model_plot(training_results):
    # Get the model train history
    model_train_history = training_results.history
    # Get the number of epochs the training was run for
    num_epochs = len(model_train_history["loss"])

    # Plot training results
    fig = plt.figure(figsize=(15, 5))
    axs = fig.add_subplot(1, 2, 1)
    axs.set_title('Loss')
    # Plot all metrics
    for metric in ["loss", "val_loss"]:
        axs.plot(np.arange(0, num_epochs), model_train_history[metric], label=metric)
    axs.legend()

    axs = fig.add_subplot(1, 2, 2)
    axs.set_title('Accuracy')
    # Plot all metrics
    for metric in ["accuracy", "val_accuracy"]:
        axs.plot(np.arange(0, num_epochs), model_train_history[metric], label=metric)
    axs.legend()

    plt.show()

####
#Prototype/Proof of Concept Model
####

def binary_cnn_with_embeddings(sequence_length, vocab_size, embedding_dim,
                              model_name='cnn_with_embeddings'):
    model_input = keras.layers.Input(shape=(sequence_length))

    hidden = keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, name="embedding")(model_input)

    hidden = keras.layers.Conv1D(filters=256, kernel_size=5, padding="valid", activation="relu", strides=3)(hidden)
    hidden = keras.layers.GlobalMaxPooling1D()(hidden)

    hidden = keras.layers.Dense(units=128, activation="tanh")(hidden)
    hidden = keras.layers.Dense(units=64, activation="tanh")(hidden)
    hidden = keras.layers.Dense(units=32, activation="tanh")(hidden)

    output = keras.layers.Dense(units=1, activation='sigmoid')(hidden)

    # Create model
    model = Model(inputs=model_input, outputs=output, name=model_name)

    return model

learning_rate = 0.01
epochs = 10
embedding_dim = 100
optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
loss = keras.losses.BinaryCrossentropy()

model = binary_cnn_with_embeddings(1500,25000, embedding_dim)
model.compile(optimizer = optimizer, loss = loss, metrics = 'binary_accuracy')
model.fit(x = x_train, y = y_train.values, validation_data = (x_test, y_test), epochs = 5, use_multiprocessing = True)
