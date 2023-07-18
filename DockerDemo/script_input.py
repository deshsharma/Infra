#!/usr/bin/env python
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM

# Parse the input text argument
parser = argparse.ArgumentParser()
parser.add_argument("--input-text", type=str, help="Input text for text generation")
args = parser.parse_args()

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("openai-gpt")
model = AutoModelForCausalLM.from_pretrained("openai-gpt")

# Generate text
input_text = args.input_text
inputs = tokenizer(input_text, return_tensors="pt")
input_ids = inputs["input_ids"]
output = model.generate(
    input_ids,
    attention_mask=inputs["attention_mask"],
    do_sample=True,
    max_length=150,
    temperature=0.8,
    use_cache=True,
    top_p=0.9
)

# Decode and print the generated text
decoded_output = tokenizer.decode(output[0])
print(decoded_output)
