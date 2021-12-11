
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

print('Setup checks complete.../n')


#####
#Prepping Tuning Data
#####
tuning_data_path = os.path.normpath('../Data/Unlabeled_Data/Unlabeled_Data.csv')

tuning_data = pd.read_csv(tuning_data_path)

#TODO: this step should be moved to pipeline after scraping is finished
tuning_data['paragraphs'] = tuning_data['paragraphs'].apply(ast.literal_eval)
tuning_data = tuning_data.explode('paragraphs')
tuning_data = tuning_data.drop_duplicates('paragraphs')
tuning_data = tuning_data[tuning_data['paragraphs'] != '']
#end of step to move


#standardize text

print('Data Loaded')

def standardize_text(input_string):
  output_string = input_string.strip()
  output_string = output_string.lower()
  return output_string

#print('Truncating Data [REMOVE AT FINAL TRAINING]')
#tuning_data = tuning_data.loc[:1000]

print('Standardizing text...')
tuning_data = tuning_data.drop_duplicates('paragraphs')
tuning_data['paragraphs'] = tuning_data['paragraphs'].apply(standardize_text)


print('Loading tokenizer...')
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

print('tokenizing...')
fine_tuning_tokens = tokenizer(list(tuning_data['paragraphs']), truncation=True, padding = True)

print('Converting to tensorslices...')
tuning_data = tf.data.Dataset.from_tensor_slices(fine_tuning_tokens)


######
#Model Tuning
#####
print('/nInitializing Model...')
BERT = TFAutoModelForTokenClassification.from_pretrained('distilbert-base-uncased')


def mask_tokens(inputs, mlm_probability, tokenizer, special_tokens_mask):
  """
  Prepare masked tokens inputs/labels for masked language modeling: 80% MASK, 10% random, 10% original.
  """
  labels = np.copy(inputs)
  # We sample a few tokens in each sequence for MLM training (with probability `self.mlm_probability`)
  probability_matrix = np.random.random_sample(labels.shape)
  special_tokens_mask = special_tokens_mask.astype(np.bool_)

  probability_matrix[special_tokens_mask] = 0.0
  masked_indices = probability_matrix > (1 - mlm_probability)
  labels[~masked_indices] = -100  # We only compute loss on masked tokens

  # 80% of the time, we replace masked input tokens with tokenizer.mask_token ([MASK])
  indices_replaced = (np.random.random_sample(labels.shape) < 0.8) & masked_indices
  inputs[indices_replaced] = tokenizer.convert_tokens_to_ids(tokenizer.mask_token)

  # 10% of the time, we replace masked input tokens with random word
  indices_random = (np.random.random_sample(labels.shape) < 0.5) & masked_indices & ~indices_replaced
  random_words = np.random.randint(low=0, high=len(tokenizer), size=np.count_nonzero(indices_random), dtype=np.int64)
  inputs[indices_random] = random_words

  # The rest of the time (10% of the time) we keep the masked input tokens unchanged
  return inputs, labels


"""
fine_tuning_tokens = tokenizer.batch_encode_plus(
        fine_tuning_file,
        return_tensors='tf',
        add_special_tokens = True, # add [CLS], [SEP]
        return_token_type_ids=True,
        padding='max_length',
        max_length=sequence_length_BERT,
        return_attention_mask = True,
        truncation='longest_first'
    )
    """


