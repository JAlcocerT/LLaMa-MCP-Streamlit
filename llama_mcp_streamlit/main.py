import streamlit as st
import asyncio

async def main():
    st.set_page_config(layout="wide")

    with st.sidebar:
        st.title("Configuration")

        # Available Tools (Dummy Data)
        st.subheader("Available Tools")
        with st.expander("Tool List", expanded=False):
            st.markdown("- *Tool1*: Example tool description")
            st.markdown("- *Tool2*: Another tool description")

        # Model Selection (Dummy Data)
        AVAILABLE_MODELS = ["Model1", "Model2"]
        selected_model = st.selectbox("Select Model", AVAILABLE_MODELS)

        # Add Model Input (Non-functional)
        new_model = st.text_input("Add New Model")
        if st.button("Add Model"):
            st.warning("This is a dummy. No models are actually added.")

        # API Configuration (Dummy Fields)
        st.subheader("API Configuration")
        api_endpoint = st.text_input("API Endpoint", "https://dummy.api.endpoint")
        api_key = st.text_input("API Key", "", type="password")

    st.title("LLM Assistant (Dummy Version)")
    st.write("Enter your query below to interact with the dummy interface.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history (Dummy)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Enter your prompt")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Dummy response
        dummy_response = "This is a dummy response. No real processing is done."
        st.session_state.messages.append({"role": "assistant", "content": dummy_response})

        with st.chat_message("assistant"):
            st.markdown(dummy_response)

if __name__ == "__main__":
    asyncio.run(main())
