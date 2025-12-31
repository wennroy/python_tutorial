# 第三章：Memory 与 RAG - 让 AI 拥有记忆和知识

> 🎯 **学习目标**
> - 理解为什么 AI 需要 Memory
> - 掌握不同类型的 Memory 实现
> - 深入理解 RAG (检索增强生成) 的原理
> - 构建一个能"开卷考试"的 AI 助手

---

## 1. 引言：AI 的"金鱼记忆"问题

默认情况下，LLM 是 **无状态** 的——它不记得之前的对话。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 第一轮对话
response1 = llm.invoke("我叫小明")
print(response1.content)  # "你好小明！有什么可以帮你的？"

# 第二轮对话
response2 = llm.invoke("我叫什么名字？")
print(response2.content)  # "抱歉，我不知道你的名字..."  😱
```

这就是为什么我们需要 **Memory**。

---

## 2. Memory：让对话有上下文

### 2.1 Memory 的工作原理

```
用户输入 ──┬──> 从 Memory 获取历史 ──> 组装完整 Prompt ──> LLM ──> 响应
           │                                                      │
           └──────────────── 保存到 Memory <────────────────────────┘
```

### 2.2 对话缓冲 Memory (最简单)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 创建模型和提示模板
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm

# 存储会话历史的字典
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 包装链以支持历史
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 使用
config = {"configurable": {"session_id": "user_123"}}

response1 = chain_with_history.invoke(
    {"input": "我叫小明，我是一名Python开发者"},
    config=config
)
print(response1.content)

response2 = chain_with_history.invoke(
    {"input": "我叫什么？我的职业是什么？"},
    config=config
)
print(response2.content)  # 现在它记得了！🎉
```

### 2.3 带窗口的 Memory (节省 Token)

历史消息太多会超出 Token 限制，我们可以只保留最近 N 轮对话：

```python
from langchain_core.chat_history import InMemoryChatMessageHistory

class WindowedChatHistory(InMemoryChatMessageHistory):
    """只保留最近 K 条消息的历史"""
    
    def __init__(self, k: int = 10):
        super().__init__()
        self.k = k
    
    def add_message(self, message):
        super().add_message(message)
        # 保持窗口大小
        while len(self.messages) > self.k:
            self.messages.pop(0)

# 使用
def get_windowed_history(session_id: str, k: int = 6):
    if session_id not in store:
        store[session_id] = WindowedChatHistory(k=k)
    return store[session_id]
```

### 2.4 摘要 Memory (超长对话)

对于很长的对话，可以让 AI 自动总结历史：

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class SummaryMemory:
    """使用摘要来压缩对话历史"""
    
    def __init__(self):
        self.summary = ""
        self.recent_messages = []
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        
    def add_exchange(self, human_msg: str, ai_msg: str):
        self.recent_messages.append(f"Human: {human_msg}")
        self.recent_messages.append(f"AI: {ai_msg}")
        
        # 当消息超过阈值时，进行摘要
        if len(self.recent_messages) > 10:
            self._summarize()
    
    def _summarize(self):
        prompt = ChatPromptTemplate.from_template(
            """请将以下对话历史和新消息整合成一个简洁的摘要：

之前的摘要：{summary}

新的对话：
{messages}

请输出更新后的摘要（100字以内）："""
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "summary": self.summary or "（无）",
            "messages": "\n".join(self.recent_messages)
        })
        
        self.summary = result.content
        self.recent_messages = []  # 清空已总结的消息
    
    def get_context(self) -> str:
        context_parts = []
        if self.summary:
            context_parts.append(f"对话摘要：{self.summary}")
        if self.recent_messages:
            context_parts.append("最近的对话：\n" + "\n".join(self.recent_messages))
        return "\n\n".join(context_parts)
```

---

## 3. RAG：让 AI "开卷考试"

### 3.1 什么是 RAG？

**RAG (Retrieval-Augmented Generation)** = 检索 + 生成

想象你参加一场开卷考试：
1. 📚 **检索 (Retrieval)**：快速翻找相关的书页
2. 📝 **生成 (Generation)**：基于找到的内容作答

```
用户问题 ──> 向量搜索 ──> 找到相关文档 ──> 组装 Prompt ──> LLM ──> 回答
                │
                └── 知识库（文档、数据库等）
```

### 3.2 向量嵌入 (Embedding) 基础

```python
from langchain_openai import OpenAIEmbeddings

# 创建嵌入模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 文本转向量
text = "Python 是一种编程语言"
vector = embeddings.embed_query(text)

print(f"向量维度: {len(vector)}")  # 1536
print(f"向量示例: {vector[:5]}")   # [0.012, -0.034, ...]

# 批量处理
texts = ["Python", "Java", "苹果", "香蕉"]
vectors = embeddings.embed_documents(texts)

# 相似度计算
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Python 和 Java 应该比 Python 和香蕉更相似
sim_py_java = cosine_similarity(vectors[0], vectors[1])
sim_py_banana = cosine_similarity(vectors[0], vectors[3])

print(f"Python vs Java: {sim_py_java:.3f}")    # ~0.8
print(f"Python vs 香蕉: {sim_py_banana:.3f}")  # ~0.3
```

### 3.3 向量数据库：Chroma 入门

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 准备文档
documents = [
    Document(
        page_content="Python 是一种高级编程语言，以简洁易读著称",
        metadata={"source": "wiki", "topic": "programming"}
    ),
    Document(
        page_content="FastAPI 是一个现代的 Python Web 框架，支持异步",
        metadata={"source": "docs", "topic": "web"}
    ),
    Document(
        page_content="Pandas 是 Python 数据分析的核心库",
        metadata={"source": "tutorial", "topic": "data"}
    ),
    Document(
        page_content="LangChain 是构建 LLM 应用的框架",
        metadata={"source": "docs", "topic": "ai"}
    ),
]

# 创建向量存储
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 持久化存储
)

# 相似度搜索
results = vectorstore.similarity_search(
    query="如何进行数据分析？",
    k=2  # 返回最相关的 2 个结果
)

for doc in results:
    print(f"📄 {doc.page_content}")
    print(f"   来源: {doc.metadata}")
    print()
```

### 3.4 构建完整的 RAG 链

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. 准备向量存储
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# 2. 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 3. 定义 RAG Prompt
rag_prompt = ChatPromptTemplate.from_template("""
你是一个专业的技术助手。请基于以下参考资料回答用户的问题。

参考资料：
{context}

用户问题：{question}

回答要求：
1. 只基于提供的参考资料回答
2. 如果资料中没有相关信息，请明确说明
3. 引用时注明来源

请回答：
""")

# 4. 辅助函数：格式化检索结果
def format_docs(docs):
    return "\n\n".join([
        f"[来源: {doc.metadata.get('source', '未知')}]\n{doc.page_content}"
        for doc in docs
    ])

# 5. 构建 RAG 链
llm = ChatOpenAI(model="gpt-4o-mini")

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 6. 使用
answer = rag_chain.invoke("Python 有哪些常用的数据分析库？")
print(answer)
```

### 3.5 进阶：加载真实文档

```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载不同格式的文档
# 1. 文本文件
text_loader = TextLoader("./docs/readme.txt")
text_docs = text_loader.load()

# 2. PDF 文件
pdf_loader = PyPDFLoader("./docs/manual.pdf")
pdf_docs = pdf_loader.load()

# 3. 网页
web_loader = WebBaseLoader("https://python.org")
web_docs = web_loader.load()

# 4. 整个目录
dir_loader = DirectoryLoader(
    "./docs/",
    glob="**/*.md",
    loader_cls=TextLoader
)
dir_docs = dir_loader.load()

# 文档分割（很重要！）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 每块最大字符数
    chunk_overlap=200,    # 块之间的重叠
    separators=["\n\n", "\n", "。", ".", " ", ""]
)

splits = text_splitter.split_documents(pdf_docs)
print(f"原始文档: {len(pdf_docs)} 个")
print(f"分割后: {len(splits)} 个块")

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

---

## 4. 实战项目：个人知识库助手

让我们构建一个完整的知识库问答系统：

```python
# knowledge_assistant.py
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

class KnowledgeAssistant:
    """个人知识库助手"""
    
    def __init__(self, docs_path: str, db_path: str = "./chroma_db"):
        self.docs_path = docs_path
        self.db_path = db_path
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.store = {}
        
        # 初始化向量存储
        self.vectorstore = self._init_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        # 构建链
        self.chain = self._build_chain()
    
    def _init_vectorstore(self) -> Chroma:
        """初始化或加载向量存储"""
        if Path(self.db_path).exists():
            print("📂 加载已有的向量数据库...")
            return Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings
            )
        else:
            print("📚 创建新的向量数据库...")
            return self._create_vectorstore()
    
    def _create_vectorstore(self) -> Chroma:
        """从文档创建向量存储"""
        # 加载文档
        loader = DirectoryLoader(
            self.docs_path,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        print(f"  加载了 {len(documents)} 个文档")
        
        # 分割文档
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        splits = splitter.split_documents(documents)
        print(f"  分割成 {len(splits)} 个块")
        
        # 创建向量存储
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.db_path
        )
        print("  ✅ 向量数据库创建完成")
        
        return vectorstore
    
    def _build_chain(self):
        """构建 RAG + Memory 链"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的知识库助手。请基于提供的参考资料回答问题。

参考资料：
{context}

回答要求：
1. 优先使用参考资料中的信息
2. 如果资料不足，可以结合你的知识补充，但要说明
3. 回答要准确、简洁、有条理"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        def format_docs(docs):
            return "\n\n---\n\n".join([
                f"[{doc.metadata.get('source', '未知')}]\n{doc.page_content}"
                for doc in docs
            ])
        
        # 基础 RAG 链
        rag_chain = (
            {
                "context": lambda x: format_docs(self.retriever.invoke(x["input"])),
                "input": lambda x: x["input"],
                "history": lambda x: x.get("history", []),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        # 添加历史支持
        def get_session_history(session_id: str):
            if session_id not in self.store:
                self.store[session_id] = InMemoryChatMessageHistory()
            return self.store[session_id]
        
        return RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
    
    def chat(self, question: str, session_id: str = "default") -> str:
        """对话接口"""
        config = {"configurable": {"session_id": session_id}}
        return self.chain.invoke({"input": question}, config=config)
    
    def add_documents(self, texts: list[str], metadatas: list[dict] = None):
        """动态添加文档到知识库"""
        from langchain_core.documents import Document
        
        if metadatas is None:
            metadatas = [{"source": "user_added"} for _ in texts]
        
        documents = [
            Document(page_content=text, metadata=meta)
            for text, meta in zip(texts, metadatas)
        ]
        
        self.vectorstore.add_documents(documents)
        print(f"✅ 已添加 {len(documents)} 个文档到知识库")


# 使用示例
if __name__ == "__main__":
    # 初始化助手（指向你的文档目录）
    assistant = KnowledgeAssistant(
        docs_path="./curriculum_content",
        db_path="./my_knowledge_db"
    )
    
    # 开始对话
    print("\n🤖 知识库助手已就绪！输入 'quit' 退出\n")
    
    while True:
        question = input("你: ").strip()
        if question.lower() == 'quit':
            break
        
        answer = assistant.chat(question)
        print(f"\n助手: {answer}\n")
```

---

## 5. 动手挑战

### 挑战 1: 构建一个 FAQ 机器人

```python
# exercise_05_03.py
"""
要求：
1. 预设 10 个常见问题和答案
2. 用户提问时，找到最相关的 FAQ
3. 基于 FAQ 生成个性化回答
"""
```

### 挑战 2: 构建一个代码文档助手

```python
# exercise_05_03_code_docs.py
"""
要求：
1. 加载一个 Python 项目的所有 .py 文件
2. 构建代码知识库
3. 能回答"这个函数是做什么的"这类问题
"""
```

---

## 6. 小结与预告

### 本章要点
- ✅ Memory 让 AI 记住对话上下文
- ✅ Embedding 将文本转换为向量
- ✅ 向量数据库实现语义搜索
- ✅ RAG = 检索 + 生成

### 下一章预告
我们将学习 **Agent 与工具调用**：
- 让 AI 自主决策
- 调用外部 API
- 执行代码

---

> 🤖 **AI 助手时间**
> - **Prompt**: "帮我优化这个 RAG 系统的检索效果"
> - **Action**: 把你的代码粘贴给 Copilot，描述遇到的问题
> - **Reflection**: AI 建议的优化方向是否可行？
