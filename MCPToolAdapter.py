import os
import json
from fastmcp import Client  
class MCPToolAdapter:  
    def __init__(self, mcp_url: str):  
        self.mcp_url = mcp_url  
        self.tools_cache = None  
      
    async def get_mcp_tools_as_functions(self):  
        """将 MCP 工具转换为 OpenAI function 格式"""  
        async with Client(self.mcp_url) as client:  
            mcp_tools = await client.list_tools()  
              
            function_tools = []  
            for tool in mcp_tools:  
                function_tool = {  
                    "type": "function",  
                    "function": {  
                        "name": tool.name,  
                        "description": tool.description or "",  
                        "parameters": tool.inputSchema or {"type": "object", "properties": {}}  
                    }  
                }  
                function_tools.append(function_tool)  
              
            self.tools_cache = {tool.name: tool for tool in mcp_tools}  
            return function_tools  
      
    async def call_mcp_tool(self, tool_name: str, arguments: dict):  
        """调用 MCP 工具并返回结果"""  
        async with Client(self.mcp_url) as client:  
            result = await client.call_tool(tool_name, arguments)  
            return result.data if hasattr(result, 'data') else str(result.content[0].text)  