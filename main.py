from ReactAgent import ReactAgent
import asyncio
import os


async def main():
    """运行所有测试"""
    # 测试工具加载
    agent = ReactAgent(model='intern-latest', thinking_mode=True)
    await agent.add_tool_from_mcp("http://localhost:8001/mcp")
    print(f"成功加载工具数量: {len(agent.tools)}")

    response = await agent.run("北京的天气如何？现在几点了？将获取到的信息在当前文件夹下创建info.txt文件写入")
    print(f"助手回答: {response}")


    print(f"消息历史: \n{agent.messages}")
if __name__ == "__main__":
    asyncio.run(main())