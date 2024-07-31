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
        model="gpt-4o",  # Default model
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Streamlit app layout
st.sidebar.title("AI 챗봇 설정")
model_choice = st.sidebar.selectbox("AI 모델 선택", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"])
api_key = st.sidebar.text_input("OpenAI API 키 입력", type="password")

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("지식 파일 업로드", type=["txt"])

knowledge_base = ""
if uploaded_file is not None:
    knowledge_base = load_knowledge_base(uploaded_file)
    st.sidebar.success("지식 파일이 성공적으로 로드되었습니다!")

user_input = st.text_input("당신: ")

if st.button("전송"):
    if user_input:
        prompt = f"{knowledge_base}\n사용자: {user_input}\nAI:" if knowledge_base else f"사용자: {user_input}\nAI:"
        response = get_gpt_response(prompt, api_key)
        st.text_area("AI:", value=response, height=200)
    else:
        st.warning("전송할 메시지를 입력하세요.")
else:
    st.warning("지식 파일을 업로드하지 않아도 채팅이 가능합니다.")
