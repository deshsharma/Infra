import streamlit as st
import requests

st.title("Blenderbot Chat")

user_input = st.text_input("User: ")
if st.button("Send"):
    response = requests.post("http://blenderbot-app:5000/predict", json={"input": user_input})
    if response.status_code == 200:
        output = response.json()["output"]
        st.text_area("Bot:", value=output, height=200)
