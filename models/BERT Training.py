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

from transformers import BertTokenizer, TFBertForSequenceClassification, TFDistilBertForSequenceClassification, TFAutoModelForTokenClassification
from transformers import TFTrainer, TrainingArguments

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from transformers import AutoTokenizer, DistilBertModel


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

print('Prepairing training data...')
training_data_path = os.path.normpath('../Data/Labeled_Data.csv')
data = pd.read_csv(training_data_path)

def standardize_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text

data['segment_text'] = data['segment_text'].apply(standardize_text)

X = data['segment_text']
y = data[['3RD', 'LOCATION', 'DEMOGRAPHIC', 'CONTACT', 'IDENTIFIER', 'SSO']].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=.25, random_state=17921)

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

X_train= tokenizer(list(X_train), truncation=True, padding = True)
X_test= tokenizer(list(X_test), truncation=True, padding = True)

BERT = TFDistilBertForSequenceClassification.from_pretrained(r'models/BERT_BASE')

control = TFDistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
