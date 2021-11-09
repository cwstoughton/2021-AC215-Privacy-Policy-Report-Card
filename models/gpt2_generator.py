import tensorflow as tf
from transformers import GPT2LMHeadModel, GPT2Tokenizer #importing the main model and tokenizer 
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel, GPT2Config
import os
import requests
import zipfile
import tarfile
import time




def download_file(packet_url, base_path="", extract=False, headers=None):
  if base_path != "":
    if not os.path.exists(base_path):
      os.mkdir(base_path)
  packet_file = os.path.basename(packet_url)
  with requests.get(packet_url, stream=True, headers=headers) as r:
      r.raise_for_status()
      with open(os.path.join(base_path,packet_file), 'wb') as f:
          for chunk in r.iter_content(chunk_size=8192):
              f.write(chunk)
  
  if extract:
    if packet_file.endswith(".zip"):
      with zipfile.ZipFile(os.path.join(base_path,packet_file)) as zfile:
        zfile.extractall(base_path)
    else:
      packet_name = packet_file.split('.')[0]
      with tarfile.open(os.path.join(base_path,packet_file)) as tfile:
        tfile.extractall(base_path)


tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")


# Dowload trained model on 100 epochs and full dataset (takes around 3 hours to train)
# start_time = time.time()
# download_file("https://github.com/dlops-io/models/releases/download/v1.0/distilgpt2_covid.zip", base_path="models", extract=True)
# execution_time = (time.time() - start_time)/60.0
# print("Download execution time (mins)",execution_time)

# Load the previously trained model
loaded_model = TFGPT2LMHeadModel.from_pretrained('./models/distilgpt2_covid/')


def generate_text(input_text):
    # Input text
    # input_text = "Your location data"

    # Tokenize Input
    input_ids = tokenizer.encode(input_text, return_tensors='tf')
    print("input_ids",input_ids)

    # Generate outout
    outputs = loaded_model.generate(
        input_ids, 
        do_sample=True, 
        max_length=75, 
        top_p=0.80, 
        top_k=0
    )

    print("Generated text:")
    # display(tokenizer.decode(outputs[0], skip_special_tokens=True))
    return tokenizer.decode(outputs[0], skip_special_tokens=True)