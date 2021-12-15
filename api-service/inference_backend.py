import tensorflow as tf
import os
import numpy as np
import sys
import pandas as pd

from transformers import TFDistilBertModel, AutoTokenizer, DistilBertConfig
from tensorflow import keras
import HTML_Parser
import re

#######
# Pipeline Functions and Components
#######
max_len = 512
loss = loss = keras.losses.binary_crossentropy

def standardize_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text

def pad(array, max_length):
    return array + [0] * (max_length - len(array))

def build_component_model(transformer, max_length=512, name = 'component_model'):
    input_layer = keras.layers.Input(shape=(max_length,),
                                            name='input_ids',
                                            dtype='int32')
    embeddings = transformer([input_layer])[0]

    #cls_token = embeddings[:, 0, :]
    hidden = keras.layers.Conv1D(filters=32, kernel_size=2, padding="valid", activation="relu")(embeddings)
    hidden = keras.layers.GlobalMaxPooling1D()(hidden)
    hidden = keras.layers.Dense(units=128, activation="tanh")(hidden)
    hidden = keras.layers.Dense(units=64, activation="tanh")(hidden)
    hidden = keras.layers.Dense(units=32, activation="tanh")(hidden)



    # Define a single node that makes up the output layer (for binary classification)
    output = keras.layers.Dense(1,activation='sigmoid')(hidden)


    model = tf.keras.Model([input_layer], output, name = name)

    # Compile the model
    model.compile(optimizer = "Adam", loss=loss,  metrics = 'binary_accuracy')

    return model


#####
#Building Base DistilBERT model for later embedding layer
#####

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
base_model = TFDistilBertModel.from_pretrained("component_models/BERT_BASE_2")

config = DistilBertConfig(dropout=.2,
                          attention_dropout=.2,
                          output_hidden_states=True)

BERT = TFDistilBertModel.from_pretrained('component_models/BERT_BASE_2', config = config)

for layer in BERT.layers:
    layer.trainable = False


#############
# Class for the Ensemble Model
#############

class backend_model:
    def __init__(self):
        self.models = {}
        self.model_scores = {}

    def add_model(self, model_name, path_to_weights, model_score = None, transformer = BERT):
        model = build_component_model(transformer, name = model_name)
        model.load_weights(path_to_weights)
        self.models.update({model_name:model})
        if model_score != None:
            self.model_scores.update({model_name: model_score})


    def single_prediction(self, input_text):
        text = standardize_text(input_text)
        tokens = tokenizer.encode(truncation=True, padding = True, max_length=max_len)
        prediction = {name:float(self.models[name].predict(tokens)) for name in self.models.keys()}

        return prediction

    def policy_prediction(self,url):
        paragraphs = HTML_Parser.parse_policy(url)
        if len (paragraphs)> 1:
            #create df from parsed HTML
            df = pd.DataFrame(columns=['Text'])
            df['Text'] = paragraphs
            df['Standardized'] = df['Text'].apply(standardize_text)

            #tokenize text using BERT tokenizer
            tokens = df['Standardized'].apply(lambda x: tokenizer.encode(x, truncation=True, padding = True, max_length=max_len))
            tokens = tokens.apply(lambda x: pad(x, max_len))
            tokens = list(tokens)
            tokens = np.array(tokens)
            #create dictionary, which will be used by API to pass JSON
            for m in self.models.keys():
                df[m] = self.models[m].predict(tokens)

            preds = [
                        {
                            'category' : name,
                            'sentences': list(df[df[name] > 0.5]['Text']),
                            'score'    : 1 - ((1-(self.model_scores[name]))**len(df[df[name] > 0.5]))
                        }

                        for name in self.models.keys()
                    ]
            final_preds = {'data':preds}

        else:
            final_preds = {name: [] for name in self.models.keys()}
            for paragraph in paragraphs:
                prediction = self.single_prediction(paragraph)

                for category in prediction:
                    if prediction[category] >= 0.5:
                        final_preds[category].append(paragraph)

        return final_preds


########
#creating inference model object
########

model = backend_model()

third_party_path = os.path.normpath('component_models/3RD/3RD')
location_path = os.path.normpath('component_models/LOCATION/LOCATION')
identifier_path = os.path.normpath('component_models/IDENTIFIER/IDENTIFIER')
contacts_path = os.path.normpath('component_models/CONTACT/CONTACT')


# scores were computed in notebook and are saved in csv
# score metric is calculated as the odds of a true positive classification using Bayes rule
model_scores = pd.read_csv(os.path.normpath('component_models/model_scores.csv'))
model_scores = model_scores.set_index('Unnamed: 0').to_dict()['0']

model.add_model('identifiers', identifier_path, model_score = model_scores['IDENTIFIER'])
model.add_model('location', location_path, model_score = model_scores['LOCATION'])
model.add_model('third_party_sharing', third_party_path, model_score = model_scores['3RD'])
model.add_model('contacts', contacts_path, model_score = model_scores['CONTACT'])