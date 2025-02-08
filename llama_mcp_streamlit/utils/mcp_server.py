from mcp import StdioServerParameters

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@executeautomation/playwright-mcp-server"],
    env=None,
)