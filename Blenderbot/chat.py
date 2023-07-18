import streamlit as st
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Download and setup the model and tokenizer
tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")

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
        
        # Display the response
        st.text_area("Bot's Response:", value=output, height=100)
        
        
        
if __name__ == "__main__":
    main()
