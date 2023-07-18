import streamlit as st
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# # Download and setup the model and tokenizer
# tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
# model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")

# # Streamlit app
# def main():
#     # Set page title
#     st.title("Blenderbot Chatbot")
    
#     # User input
#     user_input = st.text_input("Enter your question:")
    
#     if st.button("Generate Response"):
#         # Tokenize the input
#         inputs = tokenizer(user_input, return_tensors="pt")
        
#         # Generate response using the model
#         response = model.generate(**inputs)
        
#         # Decode the model output
#         output = tokenizer.decode(response[0], skip_special_tokens=True)
        
#         # Display the response
#         st.text_area("Bot's Response:", value=output, height=100)
        
        
        
# if __name__ == "__main__":
#     main()


import streamlit as st
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import pymongo
import os
# Download and setup the model and tokenizer
tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")

# Retrieve the username and password from environment variables
username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")

# MongoDB connection
mongo_client = pymongo.MongoClient('mongodb://'+username+':'+password+'@mongodb-service:27017/?authSource=admin')
db = mongo_client["chatbot"]
collection = db["history"]

# Streamlit app
def main():
    # Set page title
    st.title("Blenderbot Chatbot")
    
    # User input
    user_input = st.text_input("Enter your question:")
    
    if st.button("Generate Response"):
        # Tokenize the input
        inputs = tokenizer(user_input, return_tensors="pt")
        
        # Generate response using the model
        response = model.generate(**inputs)
        
        # Decode the model output
        output = tokenizer.decode(response[0], skip_special_tokens=True)
        
        # Insert the chat history into MongoDB
        chat_entry = {
            "user_input": user_input,
            "bot_response": output
        }
        collection.insert_one(chat_entry)
        
        # Display the response
        st.text_area("Bot's Response:", value=output, height=100)
        
    # Close MongoDB connection
    mongo_client.close()

if __name__ == "__main__":
    main()
