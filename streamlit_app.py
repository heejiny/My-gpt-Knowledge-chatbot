import streamlit as st
import openai

# Streamlit app layout
st.title("📝 파일 Q&A 챗봇")

with st.sidebar:
    api_key = st.text_input("OpenAI API 키 입력", type="password")
    model_choice = st.selectbox("AI 모델 선택", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"])

uploaded_file = st.file_uploader("지식 파일 업로드", type=["txt", "md", "json", "csv", "html"])

question = st.text_input(
    "지식에 대해 질문하기",
    placeholder="짧은 요약을 해줄 수 있나요?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not api_key:
    st.info("계속하려면 OpenAI API 키를 추가하세요.")

if uploaded_file and question and api_key:
    knowledge = uploaded_file.read().decode()
    prompt = f"다음 지식을 바탕으로 질문에 답해주세요:\n\n{knowledge}\n\n질문: {question}\n답변:"

    response = openai.ChatCompletion.create(
        model=model_choice,
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key,
        max_tokens=100,
    )
    
    st.write("### 답변")
    st.write(response['choices'][0]['message']['content'])
