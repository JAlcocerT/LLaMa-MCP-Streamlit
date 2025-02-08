import streamlit as st
from utils.agent import agent_loop

async def chat_ui(client, tools, selected_model):
    st.title("LLM Assistant with MCP Tools")
    st.write("Enter your query below to interact with the LLM and MCP tools.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Enter your prompt")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        if client:
            response, messages = await agent_loop(user_input, tools, client, st.session_state.messages, selected_model)
            st.session_state.messages = messages

        with st.chat_message("assistant"):
            st.markdown(response)
