## 项目说明

基于openai和fastmcp实现一个react agent。
由于intern暂不支持mcp工具调用，因此构建一个MCPToolAdapter，用于将fastmcp中的工具适配为openai的函数调用格式。

## 项目结构

```
./
├── mcpservers
│   ├── filesystem.py   # 文件系统工具
│   ├── weather.py      # 天气和时间查询
│   └── gate.py         # 统一mcp入口，用于调用其他工具
├── ReactAgent.py       # 实现react agent的主类
├── MCPToolAdapter.py   # 用于将fastmcp工具适配为openai函数调用格式
├── main.py             # 主程序，用于运行agent
├── testmcp.py          # 测试mcp工具调用
├── .env                # 环境变量配置文件
└── Readme.md
```

## 使用方式

1. 安装依赖
   ```
   pip install openai fastmcp
   ```
2. 配置环境变量
   - 复制`.env.example`为`.env`
   - 填写internlm API密钥,在这里获取https://internlm.intern-ai.org.cn/api/tokens
3. 启动MCP服务器
   ```
   python mcpservers/weather.py     # weather是http服务，需求单独启动；filesystem是stdio，无需单独启动
   python mcpservers/gate.py        # 二合一的网关
   ```
4. 运行React Agent
   ```
   python main.py
   ```
