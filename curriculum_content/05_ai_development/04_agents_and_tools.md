# 第四章：Agent 与工具调用 - 让 AI 自主行动

> 🎯 **学习目标**
> - 理解 Agent 的核心概念：思考-行动循环
> - 掌握工具 (Tool) 的定义与使用
> - 学会构建能调用 API、执行代码的 Agent
> - 使用 LangGraph 构建更复杂的 Agent 系统

---

## 1. 引言：从"回答问题"到"解决问题"

之前我们学习的 Chain 像是一条 **流水线**——输入进去，输出出来，路径是固定的。

但真实世界的问题往往需要 **灵活应对**：
- "帮我查一下今天的天气，然后推荐穿搭"
- "分析这份数据，如果有异常就发邮件通知我"
- "搜索网上的资料，整理成报告"

这就需要 **Agent**——一个能 **自主思考、选择工具、采取行动** 的 AI。

---

## 2. Agent 的工作原理

### 2.1 ReAct 模式：思考-行动循环

```
用户: "北京今天天气怎么样？适合跑步吗？"

Agent 思考: 用户想知道天气和运动建议，我需要先获取天气信息
Agent 行动: 调用 get_weather("北京")
观察结果: {"temp": 22, "condition": "晴", "humidity": 45}

Agent 思考: 天气数据获取成功，22度晴天，湿度适中，适合户外运动
Agent 行动: 生成最终回答
最终输出: "北京今天22度，晴天，湿度45%。这是非常适合跑步的天气！..."
```

### 2.2 核心组件

```python
Agent = LLM + Tools + Memory + Prompt

# LLM: 大脑，负责思考和决策
# Tools: 手脚，负责执行具体任务
# Memory: 记忆，记住之前的对话和行动
# Prompt: 指令，告诉 Agent 如何思考和行动
```

---

## 3. 定义工具 (Tools)

### 3.1 使用装饰器定义工具

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。
    
    Args:
        city: 城市名称，如 "北京"、"上海"
    
    Returns:
        包含温度、天气状况的字符串
    """
    # 这里应该调用真实的天气 API
    # 为了演示，返回模拟数据
    weather_data = {
        "北京": {"temp": 22, "condition": "晴"},
        "上海": {"temp": 25, "condition": "多云"},
        "广州": {"temp": 30, "condition": "雷阵雨"},
    }
    
    if city in weather_data:
        data = weather_data[city]
        return f"{city}: {data['temp']}°C, {data['condition']}"
    return f"抱歉，暂无 {city} 的天气数据"

# 查看工具信息
print(f"工具名称: {get_weather.name}")
print(f"工具描述: {get_weather.description}")
print(f"参数: {get_weather.args}")
```

### 3.2 更复杂的工具：调用真实 API

```python
import requests
from langchain_core.tools import tool

@tool
def search_web(query: str, num_results: int = 5) -> str:
    """在网络上搜索信息。
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量，默认 5
    
    Returns:
        搜索结果的摘要
    """
    # 使用 SerpAPI 或其他搜索 API
    # 这里使用 DuckDuckGo 作为示例
    from duckduckgo_search import DDGS
    
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=num_results))
    
    if not results:
        return "未找到相关结果"
    
    formatted = []
    for i, r in enumerate(results, 1):
        formatted.append(f"{i}. {r['title']}\n   {r['body'][:200]}...")
    
    return "\n\n".join(formatted)

@tool
def calculate(expression: str) -> str:
    """计算数学表达式。
    
    Args:
        expression: 数学表达式，如 "2 + 2" 或 "sqrt(16)"
    
    Returns:
        计算结果
    """
    import math
    
    # 安全的数学环境
    safe_dict = {
        "abs": abs, "round": round,
        "min": min, "max": max,
        "sum": sum, "pow": pow,
        "sqrt": math.sqrt, "log": math.log,
        "sin": math.sin, "cos": math.cos,
        "pi": math.pi, "e": math.e,
    }
    
    try:
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"

@tool
def run_python_code(code: str) -> str:
    """执行 Python 代码并返回结果。
    
    Args:
        code: 要执行的 Python 代码
    
    Returns:
        代码执行结果或错误信息
    
    注意: 仅支持简单的代码片段，不支持文件操作等危险操作
    """
    import io
    import sys
    
    # 捕获输出
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        exec(code, {"__builtins__": __builtins__})
        output = sys.stdout.getvalue()
        return output if output else "代码执行成功（无输出）"
    except Exception as e:
        return f"执行错误: {type(e).__name__}: {e}"
    finally:
        sys.stdout = old_stdout
```

### 3.3 使用 Pydantic 定义结构化工具

```python
from langchain_core.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

class EmailInput(BaseModel):
    """发送邮件的参数"""
    to: str = Field(description="收件人邮箱地址")
    subject: str = Field(description="邮件主题")
    body: str = Field(description="邮件正文")
    
def send_email_func(to: str, subject: str, body: str) -> str:
    """模拟发送邮件"""
    # 实际实现会使用 smtplib
    return f"✅ 邮件已发送至 {to}\n主题: {subject}"

send_email = StructuredTool.from_function(
    func=send_email_func,
    name="send_email",
    description="发送电子邮件",
    args_schema=EmailInput,
)
```

---

## 4. 构建 Agent

### 4.1 使用 create_react_agent

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 定义工具
@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool  
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        return str(eval(expression))
    except:
        return "计算错误"

# 创建 Agent
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_current_time, calculate]

agent = create_react_agent(llm, tools)

# 使用 Agent
result = agent.invoke({
    "messages": [("human", "现在几点了？另外帮我算一下 123 * 456")]
})

# 打印结果
for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")
```

### 4.2 带系统提示的 Agent

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(model="gpt-4o-mini")

# 自定义系统提示
system_prompt = """你是一个专业的数据分析助手。

你的职责：
1. 帮助用户分析数据
2. 进行数学计算
3. 解释分析结果

工作原则：
- 在执行任何操作前，先解释你的计划
- 每步操作后，说明结果意味着什么
- 如果遇到问题，主动提出替代方案
"""

agent = create_react_agent(
    llm, 
    tools,
    state_modifier=system_prompt  # 添加系统提示
)
```

### 4.3 Agent 与 Memory 结合

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# 创建带记忆的 Agent
llm = ChatOpenAI(model="gpt-4o-mini")
memory = MemorySaver()

agent = create_react_agent(
    llm,
    tools,
    checkpointer=memory  # 添加记忆
)

# 使用时指定 thread_id 来维持会话
config = {"configurable": {"thread_id": "user_123"}}

# 第一轮对话
result1 = agent.invoke(
    {"messages": [("human", "我叫小明，我是数据分析师")]},
    config=config
)

# 第二轮对话 - Agent 会记住之前的信息
result2 = agent.invoke(
    {"messages": [("human", "我是谁？我的职业是什么？")]},
    config=config
)
```

---

## 5. LangGraph：构建复杂的 Agent 系统

### 5.1 什么是 LangGraph？

LangGraph 是 LangChain 团队开发的框架，用于构建 **有状态的、多步骤的 AI 应用**。

它把 Agent 的行为建模为 **状态图 (State Graph)**：

```
        ┌─────────────┐
        │   开始      │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   思考      │◄──────────────┐
        └──────┬──────┘               │
               │                      │
        ┌──────▼──────┐               │
        │  需要工具？  │               │
        └──────┬──────┘               │
          是 / │ \ 否                 │
             │   │                    │
    ┌────────▼───▼────────┐           │
    │      调用工具       │───────────┘
    └─────────────────────┘
               │
        ┌──────▼──────┐
        │    结束      │
        └─────────────┘
```

### 5.2 基础概念

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add]  # 消息列表，新消息追加
    next_action: str                 # 下一步动作

# 2. 定义节点（处理函数）
def think(state: AgentState) -> AgentState:
    """思考下一步"""
    # ... 调用 LLM 决定下一步
    return {"next_action": "use_tool"}

def use_tool(state: AgentState) -> AgentState:
    """使用工具"""
    # ... 执行工具调用
    return {"messages": [result]}

# 3. 构建图
graph = StateGraph(AgentState)

# 添加节点
graph.add_node("think", think)
graph.add_node("use_tool", use_tool)

# 添加边
graph.add_edge(START, "think")
graph.add_conditional_edges(
    "think",
    lambda state: state["next_action"],
    {
        "use_tool": "use_tool",
        "finish": END,
    }
)
graph.add_edge("use_tool", "think")

# 4. 编译
app = graph.compile()
```

### 5.3 实战：多工具协作 Agent

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Literal
from operator import add

# 定义工具
@tool
def search_database(query: str) -> str:
    """在数据库中搜索信息"""
    # 模拟数据库搜索
    data = {
        "用户数": "10,234",
        "日活": "3,456",
        "收入": "¥123,456",
    }
    for key, value in data.items():
        if key in query:
            return f"{key}: {value}"
    return "未找到相关数据"

@tool
def generate_chart(data: str, chart_type: str = "bar") -> str:
    """生成图表"""
    return f"✅ 已生成 {chart_type} 图表，数据: {data}"

@tool
def send_report(content: str, recipients: str) -> str:
    """发送报告"""
    return f"✅ 报告已发送给 {recipients}"

tools = [search_database, generate_chart, send_report]

# 定义状态
class State(TypedDict):
    messages: Annotated[list, add]

# 创建 LLM
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# 定义节点
def call_llm(state: State):
    """调用 LLM"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> Literal["tools", "end"]:
    """决定是否继续"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# 构建图
graph = StateGraph(State)

graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "llm")

# 编译
agent = graph.compile()

# 使用
result = agent.invoke({
    "messages": [
        HumanMessage(content="查询用户数，生成柱状图，然后发送给 manager@company.com")
    ]
})

for msg in result["messages"]:
    if hasattr(msg, "content") and msg.content:
        print(f"{msg.type}: {msg.content}")
```

### 5.4 进阶：人机协作 (Human-in-the-Loop)

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

# ... 使用前面的 State 和节点定义 ...

# 添加人工审核节点
def human_review(state: State):
    """等待人工审核"""
    # 这个节点会暂停，等待人工输入
    return state

# 构建带审核的图
graph = StateGraph(State)
graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))
graph.add_node("human_review", human_review)

# 添加中断点
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "human_review")  # 工具执行后，等待人工审核
graph.add_edge("human_review", "llm")

# 使用 checkpointer 支持暂停和恢复
memory = MemorySaver()
agent = graph.compile(
    checkpointer=memory,
    interrupt_before=["human_review"]  # 在人工审核前暂停
)

# 执行到中断点
config = {"configurable": {"thread_id": "task_1"}}
result = agent.invoke(
    {"messages": [HumanMessage(content="发送重要报告给全体员工")]},
    config=config
)

print("⏸️ Agent 已暂停，等待人工审核...")
print("工具执行结果:", result["messages"][-1].content)

# 人工审核后继续
user_approval = input("是否批准继续？(yes/no): ")
if user_approval.lower() == "yes":
    # 继续执行
    result = agent.invoke(None, config=config)
    print("✅ 任务完成")
```

---

## 6. 实战项目：智能研究助手

```python
# research_assistant.py
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# 定义研究工具
@tool
def search_arxiv(query: str, max_results: int = 3) -> str:
    """搜索 arXiv 学术论文。
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量
    """
    import arxiv
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    results = []
    for paper in search.results():
        results.append(f"""
📄 {paper.title}
   作者: {', '.join([a.name for a in paper.authors[:3]])}
   摘要: {paper.summary[:200]}...
   链接: {paper.pdf_url}
""")
    
    return "\n".join(results) if results else "未找到相关论文"

@tool
def search_wikipedia(query: str) -> str:
    """搜索 Wikipedia 获取背景知识。
    
    Args:
        query: 搜索主题
    """
    import wikipedia
    wikipedia.set_lang("zh")
    
    try:
        page = wikipedia.page(query)
        return f"""
📖 {page.title}

{page.summary}

🔗 {page.url}
"""
    except wikipedia.exceptions.DisambiguationError as e:
        return f"该词条有多个含义: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return "未找到相关页面"

@tool
def take_notes(topic: str, content: str) -> str:
    """记录研究笔记。
    
    Args:
        topic: 笔记主题
        content: 笔记内容
    """
    # 实际应用中可以保存到文件或数据库
    return f"✅ 已记录关于「{topic}」的笔记"

@tool
def generate_summary(notes: str) -> str:
    """根据收集的信息生成研究摘要。
    
    Args:
        notes: 收集的所有笔记内容
    """
    return "正在生成摘要..."  # 实际由 LLM 处理

# 创建研究助手
llm = ChatOpenAI(model="gpt-4o")
tools = [search_arxiv, search_wikipedia, take_notes, generate_summary]
memory = MemorySaver()

system_prompt = """你是一个专业的研究助手，帮助用户进行学术研究。

工作流程：
1. 理解用户的研究问题
2. 先搜索 Wikipedia 获取背景知识
3. 再搜索 arXiv 获取最新论文
4. 记录关键信息
5. 最后生成研究摘要

注意事项：
- 每次搜索后，总结关键发现
- 如果信息不足，主动进行更多搜索
- 最终输出结构化的研究报告
"""

research_agent = create_react_agent(
    llm,
    tools,
    state_modifier=system_prompt,
    checkpointer=memory
)

# 使用
def research(topic: str, session_id: str = "default"):
    config = {"configurable": {"thread_id": session_id}}
    
    print(f"🔍 开始研究: {topic}\n")
    
    result = research_agent.invoke(
        {"messages": [("human", f"请帮我研究: {topic}")]},
        config=config
    )
    
    # 提取最终回答
    final_answer = result["messages"][-1].content
    print(f"\n📋 研究报告:\n{final_answer}")
    
    return result

# 示例
if __name__ == "__main__":
    research("大语言模型的最新进展")
```

---

## 7. 动手挑战

### 挑战 1: 构建一个代码助手 Agent

```python
# exercise_05_04.py
"""
要求：
1. 能执行 Python 代码
2. 能读写文件
3. 能搜索 Stack Overflow
4. 能解释错误并建议修复
"""
```

### 挑战 2: 构建一个数据分析 Agent

```python
# exercise_05_04_data_agent.py
"""
要求：
1. 能加载 CSV 文件
2. 能使用 pandas 进行数据分析
3. 能生成可视化图表
4. 能自动生成分析报告
"""
```

---

## 8. 小结与预告

### 本章要点
- ✅ Agent = LLM + Tools + Memory
- ✅ 工具让 AI 具备执行能力
- ✅ LangGraph 构建复杂的 Agent 工作流
- ✅ Human-in-the-Loop 实现人机协作

### 下一章预告
我们将进入 **实战项目阶段**：
- 构建一个完整的 AI 应用
- 部署到生产环境

---

> 🤖 **AI 助手时间**
> - **Prompt**: "帮我设计一个能自动写周报的 Agent，需要哪些工具？"
> - **Action**: 和 Copilot 讨论 Agent 的设计
> - **Reflection**: Agent 的能力边界在哪里？哪些任务适合 Agent？
