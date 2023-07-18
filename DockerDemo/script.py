from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("openai-gpt")
model = AutoModelForCausalLM.from_pretrained("openai-gpt")

# Generate text
input_text = "I have a cute dog"
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
print(tokenizer.decode(output[0]))