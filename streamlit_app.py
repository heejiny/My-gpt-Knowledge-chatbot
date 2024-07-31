import streamlit as st
import openai
import os

# Function to load the knowledge base from the uploaded file
def load_knowledge_base(file):
    return file.read().decode("utf-8")

# Function to get a response from the GPT model
def get_gpt_response(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Streamlit app layout
st.sidebar.title("AI Chatbot Configuration")
model_choice = st.sidebar.selectbox("Select AI Model", ["gpt-3.5-turbo", "gpt-4"])
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload Knowledge File", type=["txt"])

if uploaded_file is not None:
    knowledge_base = load_knowledge_base(uploaded_file)
    st.sidebar.success("Knowledge file loaded successfully!")

    user_input = st.text_input("You: ")
    
    if st.button("Send"):
        if user_input:
            prompt = f"{knowledge_base}\nUser: {user_input}\nAI:"
            response = get_gpt_response(prompt, api_key)
            st.text_area("AI:", value=response, height=200)
        else:
            st.warning("Please enter a message to send.")
else:
    st.warning("Please upload a knowledge file to start chatting.")
