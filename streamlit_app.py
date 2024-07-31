from openai import OpenAI
import streamlit as st

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "어떻게 도와드릴까요?"}]
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if "knowledge_file" not in st.session_state:
    st.session_state.knowledge_file = None

# 사이드바 설정
with st.sidebar:
    st.title("📝 Oh My Knowledge GPT")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[OpenAI API 키 얻기](https://platform.openai.com/account/api-keys)"
    
    # 모델 선택
    st.session_state.model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o"])
    
    # API 키 및 모델 선택 상태 표시
    if openai_api_key:
        st.write("API 키가 인식되었습니다.", unsafe_allow_html=True)
    st.write(f"powered by {st.session_state.model}", unsafe_allow_html=True)
    

# 메인 화면 설정
st.title("💬 Oh My Knowledge GPT")
st.caption("🚀 OpenAI 기반의 Streamlit 챗봇")

# Knowledge 파일 업로더
knowledge_file = st.file_uploader("Knowledge 파일 업로드", type=["txt", "pdf", "docx", "md"], key="knowledge_file_uploader")
if knowledge_file:
    st.session_state.knowledge_file = knowledge_file
    st.success("Knowledge 파일이 업로드되었습니다.")

# 채팅 메시지 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요:"):
    if not openai_api_key:
        st.info("계속하려면 OpenAI API 키를 입력하세요.")
        st.stop()

    # Knowledge 파일 내용 읽기
    knowledge_content = ""
    if st.session_state.knowledge_file:
        knowledge_content = st.session_state.knowledge_file.read().decode()

    # 클라이언트 초기화 및 메시지 추가
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # AI 응답 생성
    messages = [
        {"role": "system", "content": f"Knowledge: {knowledge_content}"},
        *st.session_state.messages
    ]
    response = client.chat.completions.create(model=st.session_state.model, messages=messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# 채팅 입력창 하단에 파일 추가 기능
additional_file = st.file_uploader("파일 추가", type=["txt", "pdf", "docx"], key="additional_file")
if additional_file:
    additional_content = additional_file.read().decode()
    st.session_state.messages.append({"role": "user", "content": f"추가 정보: {additional_content}"})
    st.success("추가 파일이 업로드되어 대화에 포함되었습니다.")
