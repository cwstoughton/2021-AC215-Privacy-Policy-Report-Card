import tensorflow as tf
import os
import numpy as np
from Model_Prototypes import binary_cnn_with_embeddings
from Pipeline.Training_Data_Pipeline import standardize_text, text_vectorizer


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
        text_vector = text_vectorizer.apply(text)
        text_vector = np.array([text_vector,])
        prediction = {name:self.models[name].predict(text_vector)[0][0] for name in self.models.keys()}

        return prediction


model = backend_model()
third_party_path = os.path.normpath('Prototype_Model_Weights/third_party_model/third_party_model')
location_path = os.path.normpath('Prototype_Model_Weights/location_model/location_model')
identifier_path = os.path.normpath('Prototype_Model_Weights/identifier_model/Best_Identifier_Model')

model.add_model('IDENTIFIERS', identifier_path)
model.add_model('LOCATION', location_path)
model.add_model('3RD_PARTY', third_party_path)