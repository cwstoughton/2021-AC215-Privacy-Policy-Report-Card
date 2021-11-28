import tensorflow as tf
import os
import numpy as np
import sys
sys.path.append(os.path.normpath('../../Demo'))

from demo_model_builder import binary_cnn_with_embeddings, standardize_text, text_vectorizer

import HTML_Parser

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

    def policy_prediction(self,url):
        final_preds = {name : [] for name in self.models.keys()}
        paragraphs = HTML_Parser.parse_policy(url)

        for paragraph in paragraphs:
                prediction = self.single_prediction(paragraph)

                for category in prediction:
                    if prediction[category] >= 0.5:
                        final_preds[category].append(paragraph)

        return final_preds


model = backend_model()
third_party_path = os.path.normpath('../../Demo/Demo_Model_Weights/third_party_model/third_party_model')
location_path = os.path.normpath('../../Demo/Demo_Model_Weights/location_model/location_model')
identifier_path = os.path.normpath('../../Demo/Demo_Model_Weights/identifier_model/Best_Identifier_Model')

model.add_model('IDENTIFIERS', identifier_path)
model.add_model('LOCATION', location_path)
model.add_model('3RD_PARTY', third_party_path)