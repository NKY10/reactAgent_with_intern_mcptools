from fastmcp import FastMCP  
import json  
import os  
from pathlib import Path  
  
# 创建MCP服务器  
mcp = FastMCP(name="weather")  
  
@mcp.tool  
def get_weather(city: str) -> dict:  
    """获取指定城市的天气信息"""  
    # 模拟天气数据  
    weather_data = {  
        "北京": {"temperature": 15, "condition": "晴天", "humidity": 45},  
        "上海": {"temperature": 18, "condition": "多云", "humidity": 60},  
        "武汉": {"temperature": 25, "condition": "小雨", "humidity": 80}  
    }  
    return {  
        "city": city,  
        "weather": weather_data.get(city, {"temperature": 20, "condition": "未知", "humidity": 50})  
    }  
@mcp.tool  
def get_time() -> str:  
    """获取当前时间"""  
    import datetime  
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
if __name__ == "__main__":  
    mcp.run(transport="http", port=8000)