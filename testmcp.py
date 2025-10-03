from fastmcp import Client  
import asyncio  
# 配置多个MCP服务器  
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
  
async def use_multi_server():  
    client = Client(config)  
      
    async with client:  
        # 工具会自动添加服务器名称前缀  
        weather = await client.call_tool("weather_get_weather", {"city": "上海"})  
        files = await client.call_tool("filesystem_list_files", {"directory": "."})  
          
        print(f"天气: {weather.data}")  
        print(f"文件: {files.data}")
  
if __name__ == "__main__":  
    asyncio.run(use_multi_server())
