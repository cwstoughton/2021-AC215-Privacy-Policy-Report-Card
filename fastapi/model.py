from transformers import GPT2Tokenizer, TFGPT2LMHeadModel


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        

# Tokenize Input
model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

def generate(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors='tf')
       
    # max_length is the maximum length of the whole text, including input words and generated ones.
    outputs = model.generate(input_ids, max_length=50,num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True) 
