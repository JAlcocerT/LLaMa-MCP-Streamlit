from mcp import StdioServerParameters
from openai import AsyncOpenAI
import asyncio
import streamlit as st
from config import AVAILABLE_MODELS
from utils.mcp_client import MCPClient
from utils.agent import agent_loop

async def main():
    st.set_page_config(layout="wide")

    with st.sidebar:
        st.title("Configuration")

        # Available Tools (no changes)
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
            if new_model not in AVAILABLE_MODELS and new_model != "":  # Prevent duplicate and empty entries
                AVAILABLE_MODELS.append(new_model)
                st.experimental_rerun()  # Rerun Streamlit to update the selectbox
        
        # API Configuration
        st.subheader("API Configuration")
        api_endpoint = st.text_input("API Endpoint", "https://integrate.api.nvidia.com/v1")
        api_key = st.text_input("API Key", "", type="password")

        # Initialize OpenAI client *inside* the sidebar
        client = AsyncOpenAI(
            base_url=api_endpoint,
            api_key=api_key,
        )


    # ... (MCP Client and tool setup - no changes)
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@executeautomation/playwright-mcp-server"],
        env=None,
    )

    async with MCPClient(server_params) as mcp_client:
        mcp_tools = await mcp_client.get_available_tools()
        tools = {
            tool.name: {
                "name": tool.name,
                "callable": mcp_client.call_tool(tool.name),
                "schema": {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                },
            }
            for tool in mcp_tools
            if tool.name != "list_tables"
        }
        st.session_state.tools = tools

        st.title("LLM Assistant with MCP Tools")
        st.write("Enter your query below to interact with the LLM and MCP tools.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input("Enter your prompt")
        if user_input:  # Removed the duplicate input check
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("user"):
                st.markdown(user_input)
            if 'client' in locals() and client:
                response, messages = await agent_loop(user_input, tools, client, st.session_state.messages, selected_model) # Pass the full message history
                st.session_state.messages = messages

            with st.chat_message("assistant"):
                st.markdown(response)

if __name__ == "__main__":
    asyncio.run(main())
