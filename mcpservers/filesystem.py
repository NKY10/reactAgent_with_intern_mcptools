from fastmcp import FastMCP  
import json  
import os  
from pathlib import Path  
  
# 创建MCP服务器  
mcp = FastMCP(name="filesystem")  

@mcp.tool  
def list_files(directory: str = ".") -> list[str]:  
    """列出指定目录下的文件"""  
    try:  
        path = Path(directory)  
        if path.exists() and path.is_dir():  
            return [f.name for f in path.iterdir()]  
        return []  
    except Exception as e:  
        return [f"错误: {str(e)}"]  
  
@mcp.tool  
def read_file(filepath: str) -> str:  
    """读取文件内容"""  
    try:  
        with open(filepath, 'r', encoding='utf-8') as f:  
            return f.read()  
    except Exception as e:  
        return f"读取文件失败: {str(e)}"  
  
@mcp.tool  
def write_file(filepath: str, content: str) -> str:  
    """写入文件内容"""  
    try:  
        with open(filepath, 'w', encoding='utf-8') as f:  
            f.write(content)  
        return f"成功写入文件: {filepath}"  
    except Exception as e:  
        return f"写入文件失败: {str(e)}"  
  
if __name__ == "__main__":  
    mcp.run(transport="stdio")