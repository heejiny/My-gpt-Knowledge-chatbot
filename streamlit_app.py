import streamlit as st
import openai

# Function to load the knowledge base from the uploaded file
def load_knowledge_base(file):
    return file.read().decode("utf-8")

# Function to get a response from the GPT model
def get_gpt_response(prompt, api_key, model):
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,  # Set to maximum tokens
        )
        return response['choices'][0]['message']['content'], None
    except openai.error.RateLimitError:
        return None, "리미트에 도달했습니다. 잠시 후 다시 시도해주세요."

# Streamlit app layout
st.title("📝 파일 Q&A 챗봇")

with st.sidebar:
    api_key = st.text_input("OpenAI API 키 입력", type="password")
    if api_key:
        st.success("API 키가 입력되었습니다.")
    model_choice = st.selectbox("AI 모델 선택", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"])
    st.markdown(f"Powered by {model_choice}")
    if st.button("새 채팅 열기"):
        st.experimental_rerun()

uploaded_file = st.file_uploader("지식 파일 업로드", type=["txt", "md", "json", "csv", "html"])

question = st.text_input(
    "지식에 대해 질문하기",
    placeholder="짧은 요약을 해줄 수 있나요?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not api_key:
    st.info("계속하려면 OpenAI API 키를 추가하세요.")

if uploaded_file and question and api_key:
    knowledge = load_knowledge_base(uploaded_file)
    prompt = f"다음 지식을 바탕으로 질문에 답해주세요:\n\n{knowledge}\n\n질문: {question}\n답변:"

    response, error_message = get_gpt_response(prompt, api_key, model_choice)
    
    if error_message:
        st.error(error_message)
    else:
        st.write("### 답변")
        st.write(response)

# Allow users to upload additional files for reference during the chat
additional_file = st.file_uploader("참고 자료 업로드", type=["txt", "md", "json", "csv", "html", "png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")

if additional_file is not None:
    st.success("참고 자료가 업로드되었습니다!")
