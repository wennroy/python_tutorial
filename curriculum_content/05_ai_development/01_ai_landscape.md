# 第一章：AI 开发全景图 - 从零到上手

> 🎯 **学习目标**
> - 理解当前 AI 开发生态的核心组件
> - 掌握 LLM (大语言模型) 的基本调用方式
> - 了解 LangChain、LangGraph 等框架的定位与作用
> - 搭建你的第一个 AI 开发环境

---

## 1. 引言：为什么现在学 AI 开发？

想象一下，你现在拥有了一个"超级实习生"——它能阅读文档、写代码、分析数据、甚至帮你做决策。这个实习生就是 **大语言模型 (LLM)**。

但问题是：**如何让这个实习生真正为你工作？**

这就是我们这个模块要解决的问题。我们不会深入 AI 的数学原理，而是聚焦于 **实战应用**：
- 如何调用各种 AI 模型
- 如何构建智能应用
- 如何让 AI 具备"记忆"和"工具使用"能力

---

## 2. AI 开发技术栈全景

```
┌─────────────────────────────────────────────────────────────────┐
│                      你的 AI 应用                                │
├─────────────────────────────────────────────────────────────────┤
│  应用层框架                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  LangChain  │  │  LangGraph  │  │   LlamaIndex │              │
│  │  (链式调用)  │  │  (状态图)    │  │   (RAG专用)  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  模型接口层                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   OpenAI    │  │  Anthropic  │  │ 本地模型     │              │
│  │   API       │  │   Claude    │  │ (Ollama等)  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  基础设施                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  向量数据库  │  │   缓存      │  │   监控      │              │
│  │ (Chroma等)  │  │  (Redis)    │  │ (LangSmith) │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 核心概念速览

| 概念 | 类比 | 作用 |
|------|------|------|
| **LLM** | 超级大脑 | 理解和生成文本 |
| **Prompt** | 工作指令 | 告诉 AI 做什么 |
| **Chain** | 工作流 | 串联多个步骤 |
| **Agent** | 自主员工 | 能自己决定用什么工具 |
| **RAG** | 开卷考试 | 让 AI 参考外部知识 |
| **Memory** | 笔记本 | 让 AI 记住对话历史 |

---

## 3. 环境搭建

### 3.1 安装核心依赖

```bash
# 创建虚拟环境
python -m venv ai_env
source ai_env/bin/activate  # macOS/Linux
# ai_env\Scripts\activate   # Windows

# 安装核心包
pip install langchain langchain-openai langchain-community
pip install langgraph
pip install python-dotenv
pip install chromadb  # 向量数据库
```

### 3.2 配置 API Key

创建 `.env` 文件（**切记不要提交到 Git！**）：

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# 国内用户可能需要配置代理
# OPENAI_API_BASE=https://your-proxy.com/v1
```

在 Python 中加载：

```python
from dotenv import load_dotenv
import os

load_dotenv()  # 从 .env 文件加载环境变量

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key 已加载: {api_key[:10]}...")  # 只打印前10位验证
```

### 3.3 验证安装

```python
# test_setup.py
from langchain_openai import ChatOpenAI

# 创建模型实例
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 简单测试
response = llm.invoke("用一句话介绍你自己")
print(response.content)
```

---

## 4. 第一个 AI 调用：Hello LLM

### 4.1 最基础的调用

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 初始化模型
llm = ChatOpenAI(
    model="gpt-4o-mini",  # 或 "gpt-4o", "gpt-3.5-turbo"
    temperature=0.7,      # 创造性程度 (0-2)
    max_tokens=1000,      # 最大输出长度
)

# 方式1: 直接调用
response = llm.invoke("Python 的 GIL 是什么？")
print(response.content)

# 方式2: 使用消息对象（推荐）
messages = [
    SystemMessage(content="你是一个 Python 专家，回答要简洁专业"),
    HumanMessage(content="解释什么是装饰器")
]
response = llm.invoke(messages)
print(response.content)
```

### 4.2 流式输出（打字机效果）

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

# 流式输出
for chunk in llm.stream("写一首关于编程的俳句"):
    print(chunk.content, end="", flush=True)
print()  # 换行
```

### 4.3 使用其他模型

```python
# Anthropic Claude
from langchain_anthropic import ChatAnthropic

claude = ChatAnthropic(model="claude-3-5-sonnet-20241022")
response = claude.invoke("Hello!")

# 本地模型 (需要先安装 Ollama)
from langchain_community.llms import Ollama

local_llm = Ollama(model="llama3.2")
response = local_llm.invoke("Hello!")
```

---

## 5. 动手挑战

### 挑战 1: 创建一个代码解释器

创建一个程序，接受用户输入的代码片段，让 AI 解释代码的功能。

```python
# exercise_05_01.py
"""
要求：
1. 接收用户输入的 Python 代码
2. 使用 LLM 解释代码功能
3. 输出要包含：功能说明、潜在问题、改进建议
"""

# TODO: 完成这个挑战
```

### 挑战 2: 多模型对比

调用不同的模型回答同一个问题，比较它们的回答质量。

---

## 6. 小结与预告

### 本章要点
- ✅ 了解了 AI 开发的技术栈全景
- ✅ 成功搭建了开发环境
- ✅ 完成了第一次 LLM 调用
- ✅ 学会了流式输出

### 下一章预告
我们将深入 **LangChain 的核心概念**：
- Prompt Templates（提示模板）
- Output Parsers（输出解析）
- Chains（链式调用）

---

> 🤖 **AI 助手时间**
> - **Prompt**: "帮我解释 LangChain 中 invoke 和 stream 方法的区别"
> - **Action**: 在 VS Code 中选中上面的代码，按 `Cmd+I` 唤起 Copilot
> - **Reflection**: 尝试让 AI 给出更多使用场景的例子
