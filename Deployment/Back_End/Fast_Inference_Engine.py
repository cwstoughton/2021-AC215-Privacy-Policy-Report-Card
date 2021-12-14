import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
import os
import numpy as np
import re
import string

import HTML_Parser
import pandas as pd

def standardize_text(input_string):
  output_string = tf.strings.lower(input_string)
  output_string = tf.strings.regex_replace(output_string, "<br />", " ")
  output_string = tf.strings.regex_replace(output_string, "[%s]" % re.escape(string.punctuation), "")
  return output_string


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

text_vectorizer = keras.layers.TextVectorization(
    standardize=standardize_text,
    max_tokens=25000,
    output_mode="int",
    output_sequence_length=1500,
)

text_data = pd.read_csv('Labeled_Data.csv')
text_data = text_data.segment_text
text_data = tf.data.Dataset.from_tensor_slices(text_data.values)
text_vectorizer.adapt(text_data.batch(64))



class backend_model:
    def __init__(self):
        self.models = {}

    def add_model(self, model_name, path_to_weights):
        model = binary_cnn_with_embeddings(1500,25000, 100, model_name = model_name)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=.01),
                      loss=tf.keras.losses.BinaryCrossentropy(),
                      metrics='binary_accuracy')
        model.load_weights(path_to_weights)

        self.models.update({model_name:model})

    def single_prediction(self, input_text):
        text = standardize_text(input_text)
        text_vector = text_vectorizer(text)
        text_vector = np.array([text_vector,])
        prediction = {name:float(self.models[name].predict(text_vector)[0][0]) for name in self.models.keys()}

        return prediction

    def policy_prediction(self, url):
        paragraphs = HTML_Parser.parse_policy(url)
        if len(paragraphs) > 1:
            df = pd.DataFrame(columns=['Text'])
            df['Text'] = paragraphs
            df['Standardized'] = standardize_text(df['Text'])
            text_vector = text_vectorizer(df['Standardized'])

            for m in self.models.keys():
                df[m] = self.models[m].predict(text_vector)

            final_preds = {name:
                               list(df[df[name] > 0.5]['Text']
                                    ) for name in self.models.keys()}

        else:
            final_preds = {name: [] for name in self.models.keys()}
            for paragraph in paragraphs:
                prediction = self.single_prediction(paragraph)

                for category in prediction:
                    if prediction[category] >= 0.5:
                        final_preds[category].append(paragraph)

        return final_preds


model = backend_model()
third_party_path = os.path.normpath('fast_models/third_party_model/third_party_model')
location_path = os.path.normpath('fast_models/location_model/location_model')
identifier_path = os.path.normpath('fast_models/identifier_model/Best_Identifier_Model')
contacts_path = os.path.normpath('fast_models/contact_model/CONTACT')

model.add_model('IDENTIFIERS', identifier_path)
model.add_model('LOCATION', location_path)
model.add_model('3RD_PARTY', third_party_path)