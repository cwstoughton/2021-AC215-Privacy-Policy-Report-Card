import pandas as pd
import os
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import re
import string

data = pd.read_csv(os.path.normpath('../Data/Labeled_Data.csv'))
x = data.segment_text
y = data.IDENTIFIER
y = y.astype(int)

x_train, x_test, y_train, y_test = train_test_split(x,y)



BATCH_SIZE = 32
TRAIN_SHUFFLE_BUFFER_SIZE = len(x_train)
VALIDATION_SHUFFLE_BUFFER_SIZE = len(x_test)
AUTOTUNE = tf.data.experimental.AUTOTUNE

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

x_train = text_vectorizer.apply(x_train)
x_test = text_vectorizer.apply(x_test)


"""
def vectorize_text(text, vectorizer=text_vectorizer, label=None):
  text = tf.expand_dims(text, -1)
  text = vectorizer(text)
  if label is None:
    return text
  else:
    return text, label

# Create TF Dataset
train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
validation_data = tf.data.Dataset.from_tensor_slices((x_test, y_test))

#############
# Train data
#############


train_data = train_data.shuffle(buffer_size=TRAIN_SHUFFLE_BUFFER_SIZE)
train_data = train_data.batch(BATCH_SIZE)
train_data = train_data.map(vectorize_text, num_parallel_calls=AUTOTUNE)
train_data = train_data.prefetch(buffer_size=AUTOTUNE)

##################
# Validation data
##################
validation_data = validation_data.shuffle(buffer_size=VALIDATION_SHUFFLE_BUFFER_SIZE)
validation_data = validation_data.batch(BATCH_SIZE)
validation_data = validation_data.map(vectorize_text, num_parallel_calls=AUTOTUNE)
validation_data = validation_data.prefetch(buffer_size=AUTOTUNE)

"""