from mcp import StdioServerParameters

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@executeautomation/playwright-mcp-server"],
    env=None,
)

# server_params = StdioServerParameters(
#     command="docker",
#     args=[
#         "run",
#         "-i",
#         "--rm",
#         "--mount", "type=bind,src=/Users/username/Desktop,dst=/projects/Desktop",
#         "--mount", "type=bind,src=/path/to/other/allowed/dir,dst=/projects/other/allowed/dir,ro",
#         "--mount", "type=bind,src=/path/to/file.txt,dst=/projects/path/to/file.txt",
#         "mcp/filesystem",
#         "/projects"
#     ],
#     env=None,
# )