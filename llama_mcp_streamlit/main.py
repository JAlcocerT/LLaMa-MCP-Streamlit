import asyncio
import streamlit as st
from ui.sidebar import sidebar
from ui.chat_ui import chat_ui
from utils.mcp_client import MCPClient
from utils.mcp_server import server_params
async def main():
    st.set_page_config(layout="wide")

    client, selected_model = sidebar()

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

        await chat_ui(client, tools, selected_model)

if __name__ == "__main__":
    asyncio.run(main())
