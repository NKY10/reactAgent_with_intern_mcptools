from fastmcp import FastMCP  
config = {  
    "mcpServers": {  
        "filesystem": {  
            "transport": "stdio",
            "command": "/Users/kun/envs/miniconda3/bin/python",  
            "args": ["/Volumes/sn580/projects/imternlm/mcpservers/filesystem.py"],
        },  
        "weather": {  
            "transport": "http",   
            "url": "http://localhost:8000/mcp",
        }  
    }  
}  
# 创建统一代理服务器  
composite_proxy = FastMCP.as_proxy(config, name="McpProxy")  
  
# 启动代理服务器供OpenAI调用  
if __name__ == "__main__":  
    composite_proxy.run(transport="http", port=8001)