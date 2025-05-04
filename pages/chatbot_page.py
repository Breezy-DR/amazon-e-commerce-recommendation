import streamlit as st
from backend.chatbot import generate_response
import time

st.markdown("# Chatbot Page")

# Simulate a bot-like response by delaying character appearances
def response_simulator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

if "chatbot_model" not in st.session_state:
    st.session_state["chatbot_model"] = "gemini-2.0-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

prompt = st.chat_input("Type your recommendation (e.g. I want a bluetooth speaker!)")
if prompt:
    # Input and display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Input and display assistant message
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = generate_response(prompt, st.session_state["chatbot_model"])
        formatted_response = response.replace('\n', '<br>')

        for chunk in response_simulator(formatted_response):
            full_response += chunk
            message_placeholder.markdown(full_response, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

