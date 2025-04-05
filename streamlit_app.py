import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🌐 재해 대응 챗봇")
st.write(
    "이 챗봇은 재난 상황에서 필요한 정보를 제공하고, 기본적인 대응 방법을 안내하는 서비스입니다. "
    "OpenAI의 GPT-3.5 모델을 기반으로 작동합니다. "
    "이용을 위해서는 OpenAI API 키가 필요합니다. [API 키 발급 링크](https://platform.openai.com/account/api-keys)"
)

# OpenAI API 키 입력 받기
openai_api_key = st.text_input("🔐 OpenAI API Key 입력", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에서 대화 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "당신은 재난/재해 대응 전문가입니다. 사용자에게 도움이 되는 정보를 제공하세요."}
        ]

    # 이전 메시지 표시
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("무엇을 도와드릴까요? 예: 지진 발생 시 행동요령"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
