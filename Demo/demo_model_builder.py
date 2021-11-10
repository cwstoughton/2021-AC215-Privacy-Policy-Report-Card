import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
import re
import string


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



data = pd.read_csv(os.path.normpath('Demo_Data.csv'))
x = data.segment_text
y = data[[
    'IDENTIFIER',
    '3RD',
    'LOCATION',
    'DEMOGRAPHIC',
    'CONTACT',
    'SSO']]


y = y.astype(int)

def standardize_text(input_string):
  output_string = tf.strings.lower(input_string)
  output_string = tf.strings.regex_replace(output_string, "<br />", " ")
  output_string = tf.strings.regex_replace(output_string, "[%s]" % re.escape(string.punctuation), "")
  return output_string

text_vectorizer = keras.layers.TextVectorization(
    standardize=standardize_text,
    max_tokens=25000,
    output_mode="int",
    output_sequence_length=1500,
)

text_data = tf.data.Dataset.from_tensor_slices(x.values)
text_vectorizer.adapt(text_data.batch(64))
