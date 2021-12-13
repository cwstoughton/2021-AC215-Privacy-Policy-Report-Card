#####
#Imports and Setup
####
import os
import ast
import re
import string

import pandas as pd
import numpy as np
import math

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.utils.layer_utils import count_params

from transformers import BertTokenizer, TFBertForSequenceClassification,TFDistilBertForMaskedLM , TFDistilBertModel, TFDistilBertForSequenceClassification, TFAutoModelForTokenClassification, DistilBertConfig
from transformers import TFTrainer, TrainingArguments

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from transformers import AutoTokenizer, DistilBertModel, pipeline

physical_devices = tf.config.list_physical_devices('GPU')

tf.config.experimental.set_memory_growth(physical_devices[0], True)


print("tensorflow version", tf.__version__)
print("keras version", tf.keras.__version__)
print("Eager Execution Enabled:", tf.executing_eagerly())

#check that GPU is running
devices = tf.config.experimental.get_visible_devices()
print("Devices:", devices)
print(tf.config.experimental.list_logical_devices('GPU'))

print("GPU Available: ", tf.config.list_physical_devices('GPU'))
print("All Physical Devices", tf.config.list_physical_devices())

# Better performance with the tf.data API
# Reference: https://www.tensorflow.org/guide/data_performance
AUTOTUNE = tf.data.experimental.AUTOTUNE

print('Setup checks complete...\n')

print('Preparing training data...')
training_data_path = os.path.normpath('../Data/Labeled_Data.csv')
data = pd.read_csv(training_data_path)

def standardize_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text

def truncate_text(text, max_len):
    return ' '.join(text.split()[:max_len])

def pad(array, max_length):
    return array + [0] * (max_length - len(array))

max_len = 512

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

data['segment_text'] = data['segment_text'].apply(standardize_text)

X = data['segment_text']
y = data[['3RD', 'LOCATION', 'DEMOGRAPHIC', 'CONTACT', 'IDENTIFIER', 'SSO']].astype(int)

#X = X.apply(lambda x: truncate_text(x, max_len))

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=.25, random_state=17921)

X_train= X_train.apply(lambda x: tokenizer.encode(x, truncation=True, padding = True, max_length=max_len))
X_test= X_test.apply(lambda x: tokenizer.encode(x, truncation=True, padding = True, max_length=max_len))




X_train = X_train.apply(lambda x: pad(x,max_len))
X_test = X_test.apply(lambda x: pad(x,max_len))

X_train = list(X_train)
X_test = list(X_test)

X_train = np.array(X_train)
X_test = np.array(X_test)


config = DistilBertConfig(dropout=.2,
                          attention_dropout=.2,
                          output_hidden_states=True)

BERT = TFDistilBertModel.from_pretrained(r'models/BERT_BASE_2', config = config)

for layer in BERT.layers:
    layer.trainable = False


loss = tf.keras.losses.binary_crossentropy


def get_embeddings(transformer, max_length = 512, cls_only = False):
    input_ids_layer = keras.layers.Input(shape=(max_length,),
                                         name='input_ids',
                                         dtype='int32')
    embeddings = transformer([input_ids_layer])[0]

    if cls_only == True:
        embeddings = transformer([input_ids_layer])[0]



def build_component_model(transformer, max_length=512):
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


    model = tf.keras.Model([input_layer], output)

    # Compile the model
    model.compile(optimizer = "Adam", loss=loss,  metrics = 'binary_accuracy')

    return model



def binary_classification_head(max_length):
    input_ids_layer = keras.layers.Input(shape=(max_length,),
                                         name='input_ids',
                                         dtype='int32')
    hidden = keras.layers.Conv1D(filters=32, kernel_size=2, padding="valid", activation="relu")(embeddings)
    hidden = keras.layers.GlobalMaxPooling1D()(hidden)
    hidden = keras.layers.Dense(units=128, activation="tanh")(hidden)
    hidden = keras.layers.Dense(units=64, activation="tanh")(hidden)
    hidden = keras.layers.Dense(units=32, activation="tanh")(hidden)
    # Define a single node that makes up the output layer (for binary classification)
    output = keras.layers.Dense(1, activation='sigmoid')(hidden)
    model = tf.keras.Model([input_ids_layer], output)
    # Compile the model
    model.compile(optimizer="Adam", loss=loss, metrics='binary_accuracy')
    return model


