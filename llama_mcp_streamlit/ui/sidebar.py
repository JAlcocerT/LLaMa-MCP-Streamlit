import streamlit as st
from openai import AsyncOpenAI
from llama_mcp_streamlit.config import AVAILABLE_MODELS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def sidebar():
    with st.sidebar:
        st.title("Configuration")

        # Available Tools
        st.subheader("Available Tools")
        if "tools" in st.session_state:
            with st.expander("Tool List", expanded=False):
                for tool_name, tool_details in st.session_state.tools.items():
                    st.markdown(f"- *{tool_name}*: {tool_details['schema']['function']['description']}")
        else:
            st.write("Tools loading... Please wait.")

        # Model Selection
        selected_model = st.selectbox("Select Model", AVAILABLE_MODELS)

        # Add Model Input
        new_model = st.text_input("Add New Model")
        if st.button("Add Model"):
            if new_model not in AVAILABLE_MODELS and new_model.strip():
                AVAILABLE_MODELS.append(new_model)
                st.experimental_rerun()

        # API Configuration
        st.subheader("API Configuration")
        api_endpoint = st.text_input("API Endpoint", os.getenv("API_ENDPOINT"))
        api_key = st.text_input("API Key", os.getenv("API_KEY", ""), type="password")

        # Initialize OpenAI client
        client = AsyncOpenAI(
            base_url=api_endpoint,
            api_key=api_key,
        )

    return client, selected_model
