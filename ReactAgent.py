import os
import json
import asyncio
from tkinter import NO
from openai import OpenAI
from MCPToolAdapter import MCPToolAdapter


class ReactAgent:
    def __init__(self, model="intern-latest", thinking_mode=True):
        self.client = OpenAI(
            api_key=os.environ.get("internlm_api_key"),
            base_url=os.environ.get("internlm_api_base_url"),
        )
        self.model = model
        self.thinking_mode = thinking_mode
        self.reset()  # 初始化对话历史

    def reset(self):
        """重置对话状态"""
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions using tools when needed."}
        ]

    async def add_tool_from_mcp(self, mcp_url: str):
        adapter = MCPToolAdapter(mcp_url)
        tools = await adapter.get_mcp_tools_as_functions()
        self.tools = tools  # 注意：这里直接赋值，不是 extend（除非你要合并多个 MCP）
        self._adapter = adapter

    async def _call_tool(self, tool_name: str, arguments: dict):
        return await self._adapter.call_mcp_tool(tool_name, arguments)
    
    def _format_thinking_content(self, message):
        if self.thinking_mode is False:
            return message.content
        else:
            return "<think>\n" + message.reasoning_content + '\n</think>'+ message.content

    async def _think(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
            extra_body={
                "thinking_mode": self.thinking_mode,
            }
        )
        message = response.choices[0].message
        
        if message.tool_calls is None:
            message_dict = {
                "role": message.role,
                "content": self._format_thinking_content(message),      
            }
        else:
            message_dict = {
                "role": message.role,
                "content": self._format_thinking_content(message),       
                "tool_calls": [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,     # str格式
                        }
                    }
                    for tc in message.tool_calls
                ]
            }
        self.messages.append(message_dict)
        return message_dict

    async def _act(self, message_dict):
        """执行阶段：调用所有工具，并将结果加入对话"""
        tool_calls = message_dict.get("tool_calls", None)
        if tool_calls is None:
            return False

        for tool_call in tool_calls:
            func = tool_call["function"]
            tool_name = func["name"]
            try:
                arguments = json.loads(func["arguments"])
            except json.JSONDecodeError:
                arguments = {}

            tool_result = await self._call_tool(tool_name, arguments)

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_name,
                "content": str(tool_result),
            })
        return True



    async def run(self, user_prompt: str, max_steps: int = 5) -> str:
        """运行完整的 ReAct 循环"""
        self.reset()
        self.messages.append({"role": "user", "content": user_prompt})

        for _ in range(max_steps):
            # 🧠 Think
            message = await self._think()
            # 🤖 Act
            has_tool_calls = await self._act(message)

            # 如果没有工具调用，说明 LLM 给出了最终答案
            if not has_tool_calls:
                return message['content'] or "No answer."

        return "Failed to reach a final answer within step limit."