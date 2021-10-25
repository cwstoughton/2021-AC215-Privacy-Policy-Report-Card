import os
import requests
import zipfile
import tarfile
import shutil
import math
import json
import time
import sys
import string
import re
import numpy as np
import pandas as pd
from glob import glob
import collections
# Transformers
# from transformers import BertTokenizer, TFBertForSequenceClassification, BertConfig
# from transformers import GPT2Tokenizer, TFGPT2LMHeadModel, GPT2Config

# Read training data
df_policies = pd.read_csv('../policy_texts.csv' , index_col=0)
training_data = list(df_policies.paragraph_text)

# Generate a random sample of index
data_samples = np.random.randint(0,high=len(training_data)-1, size=100)
for i,data_idx in enumerate(data_samples):
  print(data_idx, "Text:",training_data[data_idx])

print(len(training_data))