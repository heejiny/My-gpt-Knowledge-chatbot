import streamlit as st
from openai import OpenAI
import os

# API 키를 세션 상태에 저장
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 모델 선택을 세션 상태에 저장
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"

# 대화 기록을 세션 상태에 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바 설정
with st.sidebar:
    st.title("📝 Oh My Knowledge GPT")
    
    # API 키 입력
    st.session_state.api_key = st.text_input("API Key 입력", type="password")
    
    # 모델 선택
    st.session_state.model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o"])
    
    # API 키 및 모델 선택 상태 표시
    if st.session_state.api_key:
        st.write("api key가 인식되었습니다.", unsafe_allow_html=True)
    st.write(f"powered by {st.session_state.model}", unsafe_allow_html=True)
    
    # 하루 사용량 체크 (예시로 1000 요청 제한)
    usage_limit = 1000
    current_usage = 100  # 실제 사용량을 추적하는 로직 필요
    st.write(f"오늘 사용량: {current_usage}/{usage_limit}", unsafe_allow_html=True)
    
    # 새 채팅창 열기
    if st.button("새 채팅창 열기"):
        st.session_state.messages = []
        st.experimental_rerun()

# OpenAI 클라이언트 초기화
if st.session_state.api_key:
    openai.api_key = st.session_state.api_key
else:
    st.warning("API 키를 입력하세요.")

# 메인 화면 설정
st.title("GPT-4o-mini 챗봇")

# 파일 업로더 (Knowledge 파일)
knowledge_file = st.file_uploader("Knowledge 파일 업로드", type=["txt", "pdf", "docx"], key="knowledge_file")

# 이전 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
user_input = st.chat_input("질문을 입력하세요:")

if user_input:
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Knowledge 파일 내용 읽기
    knowledge_content = ""
    if knowledge_file:
        knowledge_content = knowledge_file.read().decode()

    # AI 응답 생성
    if st.session_state.api_key:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.completions.create(
                model=st.session_state.model,
                messages=[
                    {"role": "system", "content": f"Knowledge: {knowledge_content}"},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # AI 응답을 메시지 기록에 추가
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 채팅 입력창 하단에 파일 추가 기능
additional_file = st.file_uploader("파일 추가", type=["txt", "pdf", "docx"], key="additional_file")

if additional_file:
    # 추가 파일 내용 읽기
    additional_content = additional_file.read().decode()
    # 추가 파일 내용을 AI에게 전달
    st.session_state.messages.append({"role": "user", "content": f"추가 정보: {additional_content}"})
