"""
Module that contains the command line app.
"""
import argparse
import os
# import ffmpeg
import io

# Test access


def generate(prompt):
    from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        
    input_ids = tokenizer.encode(prompt, return_tensors='tf')
    # Tokenize Input
    model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    
    # max_length is the maximum length of the whole text, including input words and generated ones.
    outputs = model.generate(input_ids, max_length=50,num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True) 

def main(args=None):

    print("Args:", args)

    # if args.download:
    #     download()
    if args.generate:
        generate()
    # if args.upload:
    #     upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(
        description='Generate text from prompt')

    # parser.add_argument("-d", "--download", action='store_true',
    #                     help="Download text prompts from GCS bucket")

    parser.add_argument("-g", "--generate", action='store_true',
                        help="Generate a text paragraph")

    # parser.add_argument("-u", "--upload", action='store_true',
    #                     help="Upload paragraph text to GCS bucket")

    args = parser.parse_args()

    main(args)

