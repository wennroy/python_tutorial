# 第二章：LangChain 核心概念精讲

> 🎯 **学习目标**
> - 掌握 Prompt Template 的设计与使用
> - 理解 Output Parser 的作用与实现
> - 学会使用 LCEL (LangChain Expression Language) 构建链
> - 能够组合多个组件构建复杂工作流

---

## 1. 引言：为什么需要 LangChain？

直接调用 LLM API 当然可以，但当你的应用变复杂时，你会遇到这些问题：

- 📝 **Prompt 管理混乱**：到处都是字符串拼接
- 🔄 **重复代码**：每次都要处理 API 调用、错误处理
- 🧩 **难以组合**：想串联多个步骤很麻烦
- 📊 **输出不可控**：LLM 返回的格式难以预测

LangChain 就是来解决这些问题的 **"胶水层"**。

---

## 2. Prompt Templates：提示词工程的基石

### 2.1 为什么需要模板？

❌ **不好的做法**：
```python
# 硬编码，难以维护
prompt = f"请用{language}语言解释{concept}，面向{audience}的读者"
```

✅ **好的做法**：
```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，回答要{style}"),
    ("human", "请解释：{question}")
])

# 复用、测试、版本管理都很方便
prompt = template.invoke({
    "role": "Python专家",
    "style": "简洁专业",
    "question": "什么是GIL？"
})
```

### 2.2 不同类型的模板

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder
)

# 1. 基础字符串模板
simple_template = PromptTemplate.from_template(
    "将以下文本翻译成{language}：\n{text}"
)

# 2. 聊天模板（推荐用于 Chat 模型）
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{profession}"),
    ("human", "{user_input}"),
])

# 3. 带示例的模板（Few-shot Learning）
examples = [
    {"input": "开心", "output": "😊"},
    {"input": "难过", "output": "😢"},
]

example_template = PromptTemplate.from_template(
    "输入: {input}\n输出: {output}"
)

few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="将情绪转换为表情符号：",
    suffix="输入: {input}\n输出:",
    input_variables=["input"]
)

# 4. 支持动态消息历史
history_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手"),
    MessagesPlaceholder(variable_name="history"),  # 动态插入历史消息
    ("human", "{input}"),
])
```

### 2.3 实战：构建一个代码审查 Prompt

```python
from langchain_core.prompts import ChatPromptTemplate

code_review_template = ChatPromptTemplate.from_messages([
    ("system", """你是一个资深代码审查专家。
请从以下维度审查代码：
1. 代码质量与可读性
2. 潜在的 Bug 或安全问题  
3. 性能优化建议
4. 最佳实践建议

输出格式要求：使用 Markdown，每个维度一个小节。"""),
    ("human", """请审查以下 {language} 代码：

```{language}
{code}
```

额外背景：{context}""")
])

# 使用
prompt = code_review_template.invoke({
    "language": "python",
    "code": """
def get_user(id):
    users = load_all_users()  # 从数据库加载所有用户
    for user in users:
        if user.id == id:
            return user
    return None
""",
    "context": "这是一个用户管理系统的一部分"
})

print(prompt)
```

---

## 3. Output Parsers：驯服 LLM 的输出

LLM 的输出是自由文本，但我们往往需要 **结构化数据**。

### 3.1 常用的 Parser 类型

```python
from langchain_core.output_parsers import (
    StrOutputParser,      # 原样输出字符串
    JsonOutputParser,     # 解析为 JSON
    PydanticOutputParser, # 解析为 Pydantic 模型
)
from langchain_core.pydantic_v1 import BaseModel, Field

# 1. 字符串解析器（默认）
str_parser = StrOutputParser()

# 2. JSON 解析器
json_parser = JsonOutputParser()

# 3. Pydantic 解析器（强类型，推荐！）
class CodeReview(BaseModel):
    """代码审查结果"""
    summary: str = Field(description="一句话总结")
    issues: list[str] = Field(description="发现的问题列表")
    score: int = Field(description="代码质量评分 1-10")
    suggestions: list[str] = Field(description="改进建议")

pydantic_parser = PydanticOutputParser(pydantic_object=CodeReview)
```

### 3.2 让 LLM 按格式输出

**关键技巧**：把格式说明注入到 Prompt 中

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

# 定义输出结构
class MovieRecommendation(BaseModel):
    title: str = Field(description="电影标题")
    year: int = Field(description="上映年份")
    reason: str = Field(description="推荐理由")
    rating: float = Field(description="评分 0-10")

# 创建解析器
parser = PydanticOutputParser(pydantic_object=MovieRecommendation)

# 创建带格式说明的 Prompt
template = ChatPromptTemplate.from_messages([
    ("system", """你是一个电影推荐专家。
{format_instructions}"""),
    ("human", "推荐一部{genre}类型的电影")
])

# 注入格式说明
prompt = template.partial(
    format_instructions=parser.get_format_instructions()
)

# 组装链
llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | parser

# 执行
result = chain.invoke({"genre": "科幻"})
print(f"推荐电影: {result.title} ({result.year})")
print(f"理由: {result.reason}")
print(f"评分: {result.rating}")
```

---

## 4. LCEL：LangChain 表达式语言

LCEL 是 LangChain 的核心创新，它让你用 **管道操作符 `|`** 组合组件。

### 4.1 基础语法

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 定义组件
prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 用管道组合（就像 Unix 命令）
chain = prompt | llm | parser

# 调用
result = chain.invoke({"topic": "程序员"})
print(result)
```

### 4.2 LCEL 的魔力：自动获得超能力

当你用 LCEL 组合组件后，自动获得：

```python
# ✅ 流式输出
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="")

# ✅ 批量处理
results = chain.batch([
    {"topic": "程序员"},
    {"topic": "产品经理"},
    {"topic": "设计师"},
])

# ✅ 异步调用
import asyncio
result = asyncio.run(chain.ainvoke({"topic": "AI"}))

# ✅ 并行批量（更快）
results = chain.batch(
    [{"topic": t} for t in ["Python", "Java", "Rust"]],
    config={"max_concurrency": 3}
)
```

### 4.3 复杂链的构建

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 并行执行多个子链
analysis_chain = RunnableParallel(
    summary=prompt_summary | llm | parser,
    sentiment=prompt_sentiment | llm | parser,
    keywords=prompt_keywords | llm | parser,
)

# 结果会是一个字典：{"summary": "...", "sentiment": "...", "keywords": "..."}

# 传递原始输入
chain_with_context = RunnableParallel(
    original=RunnablePassthrough(),  # 保留原始输入
    processed=some_chain,
)
```

### 4.4 实战：构建一个翻译+总结链

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 翻译链
translate_prompt = ChatPromptTemplate.from_template(
    "将以下文本翻译成{target_language}：\n\n{text}"
)
translate_chain = translate_prompt | llm | parser

# 总结链
summarize_prompt = ChatPromptTemplate.from_template(
    "用一句话总结以下内容：\n\n{text}"
)
summarize_chain = summarize_prompt | llm | parser

# 组合：先翻译，再总结
def create_full_chain(target_language):
    return (
        {"text": lambda x: x["text"], "target_language": lambda x: target_language}
        | translate_chain
        | (lambda translated: {"text": translated})
        | summarize_chain
    )

# 或者并行执行
parallel_chain = RunnableParallel(
    chinese=translate_prompt.partial(target_language="中文") | llm | parser,
    japanese=translate_prompt.partial(target_language="日语") | llm | parser,
    summary=summarize_prompt | llm | parser,
)

result = parallel_chain.invoke({
    "text": "LangChain is a framework for building LLM applications."
})
print(result)
# {'chinese': 'LangChain是一个构建LLM应用的框架', 
#  'japanese': 'LangChainはLLMアプリケーションを構築するためのフレームワークです', 
#  'summary': 'LangChain helps build AI apps'}
```

---

## 5. 实战项目：智能文档分析器

让我们把学到的知识整合成一个完整的项目：

```python
# document_analyzer.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableParallel

# 定义输出结构
class DocumentAnalysis(BaseModel):
    """文档分析结果"""
    title: str = Field(description="文档标题或主题")
    summary: str = Field(description="100字以内的摘要")
    key_points: list[str] = Field(description="3-5个关键要点")
    sentiment: str = Field(description="整体情感：正面/中性/负面")
    category: str = Field(description="文档类别：技术/商业/学术/新闻/其他")
    action_items: list[str] = Field(description="建议的后续行动")

# 创建分析器
class DocumentAnalyzer:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model)
        self.parser = PydanticOutputParser(pydantic_object=DocumentAnalysis)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的文档分析专家。
分析用户提供的文档，提取关键信息。

{format_instructions}"""),
            ("human", "请分析以下文档：\n\n{document}")
        ]).partial(format_instructions=self.parser.get_format_instructions())
        
        self.chain = self.prompt | self.llm | self.parser
    
    def analyze(self, document: str) -> DocumentAnalysis:
        """分析单个文档"""
        return self.chain.invoke({"document": document})
    
    def analyze_batch(self, documents: list[str]) -> list[DocumentAnalysis]:
        """批量分析文档"""
        return self.chain.batch(
            [{"document": doc} for doc in documents],
            config={"max_concurrency": 3}
        )

# 使用示例
if __name__ == "__main__":
    analyzer = DocumentAnalyzer()
    
    sample_doc = """
    Python 3.12 发布说明
    
    Python 3.12 带来了多项重要更新：
    1. 更好的错误消息，帮助开发者快速定位问题
    2. 新增 type 语句，简化类型别名定义
    3. 性能提升约 5%，得益于更优化的解释器
    4. 改进了 f-string 的语法，支持更复杂的表达式
    
    建议所有开发者在测试环境中尝试升级。
    """
    
    result = analyzer.analyze(sample_doc)
    
    print(f"📄 标题: {result.title}")
    print(f"📝 摘要: {result.summary}")
    print(f"🎯 关键点:")
    for point in result.key_points:
        print(f"   • {point}")
    print(f"😊 情感: {result.sentiment}")
    print(f"📁 类别: {result.category}")
    print(f"✅ 建议行动:")
    for action in result.action_items:
        print(f"   • {action}")
```

---

## 6. 动手挑战

### 挑战 1: 创建一个多语言翻译器

```python
# exercise_05_02.py
"""
要求：
1. 接收一段文本
2. 同时翻译成中文、日文、法文
3. 使用 RunnableParallel 并行处理
4. 输出结构化结果
"""
```

### 挑战 2: 构建一个面试题生成器

```python
# exercise_05_02_interview.py
"""
要求：
1. 输入：职位名称、难度级别
2. 输出：3道面试题，每题包含问题、考察点、参考答案
3. 使用 Pydantic 定义输出结构
"""
```

---

## 7. 小结与预告

### 本章要点
- ✅ Prompt Template 让提示词管理更规范
- ✅ Output Parser 让 LLM 输出结构化数据
- ✅ LCEL 让组件组合变得简单优雅
- ✅ 自动获得流式、批量、异步能力

### 下一章预告
我们将学习 **Memory 与 RAG**：
- 让 AI 拥有记忆
- 让 AI 参考外部知识库

---

> 🤖 **AI 助手时间**
> - **Prompt**: "帮我设计一个用于生成周报的 Prompt Template"
> - **Action**: 打开 Copilot Chat，描述你的需求
> - **Reflection**: AI 生成的模板是否考虑了所有必要的字段？
