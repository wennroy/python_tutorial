# 第五章：AI 应用实战 - 从零构建生产级项目

> 🎯 **学习目标**
> - 掌握 AI 应用的完整开发流程
> - 学会处理生产环境中的常见问题
> - 构建一个完整的、可部署的 AI 项目
> - 理解成本优化和性能调优

---

## 1. 引言：从 Demo 到产品

写一个 AI Demo 很简单，但要上线一个稳定的产品，你需要考虑：

- 💰 **成本控制**：API 调用费用、Token 使用量
- ⚡ **性能优化**：响应延迟、并发处理
- 🔒 **安全防护**：Prompt 注入、敏感信息
- 📊 **可观测性**：日志、监控、追踪
- 🔄 **容错处理**：重试、降级、超时

这一章，我们将构建一个 **完整的 AI 客服系统**，涵盖所有这些要点。

---

## 2. 项目架构设计

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户界面 (Web/API)                        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────┐
│                         FastAPI 服务                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  路由层   │  │  中间件   │  │  限流器   │  │  日志器   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────┐
│                         AI 服务层                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Agent    │  │ RAG 引擎  │  │ 缓存层   │  │ 工具集   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────┐
│                         数据层                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 向量DB   │  │ Redis    │  │ SQLite   │  │ 文件存储  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 项目结构

```
ai_customer_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py        # API 路由
│   │   └── schemas.py       # Pydantic 模型
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py         # AI Agent
│   │   ├── rag.py           # RAG 引擎
│   │   ├── tools.py         # 工具定义
│   │   └── prompts.py       # Prompt 模板
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cache.py         # 缓存服务
│   │   ├── database.py      # 数据库服务
│   │   └── monitoring.py    # 监控服务
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # 安全工具
│       └── helpers.py       # 辅助函数
├── data/
│   └── knowledge_base/      # 知识库文档
├── tests/
│   ├── __init__.py
│   └── test_agent.py
├── .env
├── requirements.txt
└── docker-compose.yml
```

---

## 3. 核心代码实现

### 3.1 配置管理 (config.py)

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    # API Keys
    openai_api_key: str
    openai_api_base: str | None = None
    
    # 模型配置
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # 数据库
    chroma_db_path: str = "./data/chroma_db"
    sqlite_db_path: str = "./data/app.db"
    redis_url: str = "redis://localhost:6379"
    
    # 性能
    cache_ttl: int = 3600  # 缓存过期时间（秒）
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    
    # 安全
    max_input_length: int = 5000
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### 3.2 安全防护 (security.py)

```python
# app/utils/security.py
import re
from typing import Tuple

class SecurityChecker:
    """安全检查器"""
    
    # Prompt 注入检测模式
    INJECTION_PATTERNS = [
        r"ignore.*previous.*instructions",
        r"disregard.*above",
        r"forget.*everything",
        r"you.*are.*now",
        r"new.*instructions",
        r"system.*prompt",
    ]
    
    # 敏感信息模式
    SENSITIVE_PATTERNS = [
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # 信用卡号
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # 邮箱
        r"\b1[3-9]\d{9}\b",  # 手机号
        r"\b\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b",  # 身份证
    ]
    
    def __init__(self):
        self.injection_regex = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
        self.sensitive_regex = [re.compile(p) for p in self.SENSITIVE_PATTERNS]
    
    def check_injection(self, text: str) -> Tuple[bool, str]:
        """检测 Prompt 注入"""
        for pattern in self.injection_regex:
            if pattern.search(text):
                return False, "检测到可疑的指令注入"
        return True, ""
    
    def mask_sensitive_info(self, text: str) -> str:
        """遮蔽敏感信息"""
        masked = text
        for pattern in self.sensitive_regex:
            masked = pattern.sub("[已隐藏]", masked)
        return masked
    
    def validate_input(self, text: str, max_length: int = 5000) -> Tuple[bool, str]:
        """验证输入"""
        if not text or not text.strip():
            return False, "输入不能为空"
        
        if len(text) > max_length:
            return False, f"输入过长，最大允许 {max_length} 字符"
        
        is_safe, msg = self.check_injection(text)
        if not is_safe:
            return False, msg
        
        return True, ""

security_checker = SecurityChecker()
```

### 3.3 缓存服务 (cache.py)

```python
# app/services/cache.py
import hashlib
import json
from typing import Any, Optional
from datetime import timedelta
import redis.asyncio as redis
from app.config import settings

class CacheService:
    """缓存服务 - 支持 Redis 和内存缓存"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}  # 内存缓存作为备份
    
    async def connect(self):
        """连接 Redis"""
        try:
            self.redis_client = await redis.from_url(
                settings.redis_url,
                decode_responses=True
            )
            await self.redis_client.ping()
            print("✅ Redis 连接成功")
        except Exception as e:
            print(f"⚠️ Redis 连接失败，使用内存缓存: {e}")
            self.redis_client = None
    
    def _generate_key(self, prefix: str, content: str) -> str:
        """生成缓存键"""
        hash_value = hashlib.md5(content.encode()).hexdigest()[:16]
        return f"{prefix}:{hash_value}"
    
    async def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        if self.redis_client:
            try:
                return await self.redis_client.get(key)
            except Exception:
                pass
        return self.memory_cache.get(key)
    
    async def set(self, key: str, value: str, ttl: int = None):
        """设置缓存"""
        ttl = ttl or settings.cache_ttl
        
        if self.redis_client:
            try:
                await self.redis_client.setex(key, ttl, value)
                return
            except Exception:
                pass
        
        self.memory_cache[key] = value
    
    async def get_llm_response(self, prompt: str) -> Optional[str]:
        """获取 LLM 响应缓存"""
        key = self._generate_key("llm", prompt)
        cached = await self.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    async def set_llm_response(self, prompt: str, response: str):
        """缓存 LLM 响应"""
        key = self._generate_key("llm", prompt)
        await self.set(key, json.dumps(response))

cache_service = CacheService()
```

### 3.4 AI Agent 核心 (agent.py)

```python
# app/core/agent.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from app.config import settings
from app.core.tools import get_customer_service_tools
from app.core.prompts import CUSTOMER_SERVICE_PROMPT
from app.services.cache import cache_service
from app.utils.security import security_checker
import logging

logger = logging.getLogger(__name__)

class CustomerServiceAgent:
    """客服 Agent"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
            request_timeout=settings.request_timeout,
        )
        
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        
        self.vectorstore = self._init_vectorstore()
        self.tools = get_customer_service_tools(self.vectorstore)
        self.memory = MemorySaver()
        
        self.agent = create_react_agent(
            self.llm,
            self.tools,
            state_modifier=CUSTOMER_SERVICE_PROMPT,
            checkpointer=self.memory,
        )
    
    def _init_vectorstore(self) -> Chroma:
        """初始化向量存储"""
        return Chroma(
            persist_directory=settings.chroma_db_path,
            embedding_function=self.embeddings,
        )
    
    async def chat(
        self,
        message: str,
        session_id: str,
        user_info: dict = None
    ) -> dict:
        """处理用户消息"""
        
        # 1. 安全检查
        is_valid, error_msg = security_checker.validate_input(
            message, 
            settings.max_input_length
        )
        if not is_valid:
            return {
                "success": False,
                "error": error_msg,
                "response": None
            }
        
        # 2. 遮蔽敏感信息（用于日志）
        safe_message = security_checker.mask_sensitive_info(message)
        logger.info(f"Session {session_id}: {safe_message[:100]}...")
        
        # 3. 检查缓存（简单问题可能有缓存）
        cached_response = await cache_service.get_llm_response(message)
        if cached_response:
            logger.info(f"Cache hit for session {session_id}")
            return {
                "success": True,
                "response": cached_response,
                "from_cache": True
            }
        
        # 4. 调用 Agent
        try:
            config = {"configurable": {"thread_id": session_id}}
            
            # 构造消息
            messages = [("human", message)]
            if user_info:
                # 注入用户上下文
                context = f"用户信息: {user_info}"
                messages = [("system", context)] + messages
            
            result = await self.agent.ainvoke(
                {"messages": messages},
                config=config
            )
            
            # 提取回复
            response = result["messages"][-1].content
            
            # 5. 缓存响应（仅缓存简单问答）
            if len(result["messages"]) <= 3:  # 没有复杂的工具调用
                await cache_service.set_llm_response(message, response)
            
            return {
                "success": True,
                "response": response,
                "from_cache": False
            }
            
        except Exception as e:
            logger.error(f"Agent error: {e}", exc_info=True)
            return {
                "success": False,
                "error": "服务暂时不可用，请稍后重试",
                "response": None
            }
    
    async def get_conversation_history(self, session_id: str) -> list:
        """获取对话历史"""
        config = {"configurable": {"thread_id": session_id}}
        state = await self.agent.aget_state(config)
        if state and state.values:
            return [
                {"role": msg.type, "content": msg.content}
                for msg in state.values.get("messages", [])
            ]
        return []

# 单例
customer_service_agent = CustomerServiceAgent()
```

### 3.5 API 路由 (routes.py)

```python
# app/api/routes.py
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
from app.core.agent import customer_service_agent
from app.services.cache import cache_service

router = APIRouter(prefix="/api/v1", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str = Field(..., min_length=1, max_length=100)
    user_info: Optional[dict] = None

class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    from_cache: bool = False

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口"""
    result = await customer_service_agent.chat(
        message=request.message,
        session_id=request.session_id,
        user_info=request.user_info
    )
    return ChatResponse(**result)

@router.get("/chat/stream")
async def chat_stream(message: str, session_id: str):
    """流式聊天接口"""
    async def generate():
        # 这里需要修改 agent 以支持流式输出
        # 简化示例：
        result = await customer_service_agent.chat(message, session_id)
        if result["success"]:
            for char in result["response"]:
                yield f"data: {char}\n\n"
                await asyncio.sleep(0.02)
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """获取对话历史"""
    history = await customer_service_agent.get_conversation_history(session_id)
    return {"session_id": session_id, "history": history}

@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """清除对话历史"""
    # 实现清除逻辑
    return {"success": True, "message": "历史已清除"}
```

### 3.6 主应用 (main.py)

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from app.api.routes import router
from app.services.cache import cache_service
from app.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("🚀 正在启动服务...")
    await cache_service.connect()
    logger.info("✅ 服务启动完成")
    
    yield
    
    # 关闭时
    logger.info("🔄 正在关闭服务...")

app = FastAPI(
    title="AI 客服系统",
    description="基于 LangChain 的智能客服 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求计时中间件
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# 注册路由
app.include_router(router)

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 4. 部署配置

### 4.1 Docker 配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./data:/app/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### 4.2 生产环境清单

```markdown
## 上线前检查清单

### 安全
- [ ] API Key 使用环境变量
- [ ] 启用 HTTPS
- [ ] 配置 CORS 白名单
- [ ] 实现 API 认证
- [ ] 启用 Rate Limiting
- [ ] 输入验证与清洗
- [ ] Prompt 注入防护

### 性能
- [ ] 配置响应缓存
- [ ] 启用连接池
- [ ] 设置合理的超时时间
- [ ] 配置并发限制

### 可观测性
- [ ] 结构化日志
- [ ] 错误追踪 (Sentry)
- [ ] API 指标监控
- [ ] LLM 调用追踪 (LangSmith)

### 运维
- [ ] 健康检查端点
- [ ] 优雅关闭
- [ ] 自动重启策略
- [ ] 数据备份
```

---

## 5. 成本优化策略

### 5.1 Token 使用优化

```python
# 1. 使用更便宜的模型处理简单任务
def select_model(task_complexity: str) -> str:
    """根据任务复杂度选择模型"""
    if task_complexity == "simple":
        return "gpt-4o-mini"  # 便宜
    elif task_complexity == "medium":
        return "gpt-4o-mini"
    else:
        return "gpt-4o"  # 复杂任务用强模型

# 2. 压缩历史消息
def compress_history(messages: list, max_tokens: int = 2000) -> list:
    """压缩对话历史"""
    # 保留最近的消息，旧消息压缩为摘要
    if len(messages) <= 6:
        return messages
    
    # 保留最新的 4 条
    recent = messages[-4:]
    
    # 旧消息压缩为摘要
    old_content = "\n".join([m.content for m in messages[:-4]])
    summary = summarize(old_content)  # 调用 LLM 摘要
    
    return [SystemMessage(content=f"之前的对话摘要: {summary}")] + recent

# 3. 缓存常见问答
COMMON_QA = {
    "营业时间": "我们的营业时间是 9:00-18:00",
    "联系方式": "您可以拨打 400-xxx-xxxx",
    # ...
}

def check_common_qa(question: str) -> Optional[str]:
    """检查是否是常见问题"""
    for key, answer in COMMON_QA.items():
        if key in question:
            return answer
    return None
```

### 5.2 调用频率控制

```python
from functools import wraps
import asyncio
from collections import defaultdict
import time

class RateLimiter:
    """简单的限流器"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        # 清理过期记录
        self.requests[key] = [
            t for t in self.requests[key] 
            if now - t < self.window
        ]
        
        if len(self.requests[key]) >= self.max_requests:
            return False
        
        self.requests[key].append(now)
        return True

rate_limiter = RateLimiter(max_requests=60, window_seconds=60)

def rate_limit(key_func):
    """限流装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            if not rate_limiter.is_allowed(key):
                raise HTTPException(429, "请求过于频繁，请稍后重试")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# 使用
@rate_limit(lambda request: request.session_id)
async def chat(request: ChatRequest):
    ...
```

---

## 6. 动手挑战

### 挑战: 完善这个客服系统

```python
# exercise_05_05.py
"""
基于本章代码，完成以下任务：

1. 添加更多工具：
   - 查询订单状态
   - 提交工单
   - 转人工客服

2. 实现会话管理：
   - 设置会话过期时间
   - 导出对话记录

3. 添加监控：
   - 统计每日请求量
   - 计算平均响应时间
   - 追踪 Token 消耗

4. 优化体验：
   - 添加打字机效果的流式输出
   - 支持多轮澄清对话
"""
```

---

## 7. 小结

### 本章要点
- ✅ 生产级 AI 应用的完整架构
- ✅ 安全防护：输入验证、Prompt 注入防护
- ✅ 性能优化：缓存、限流、模型选择
- ✅ 可观测性：日志、监控、追踪
- ✅ 部署：Docker 化、环境配置

### 你已经学会了
通过这五章的学习，你已经掌握了：

1. **基础调用**：直接使用 LLM API
2. **LangChain 核心**：Prompt、Parser、Chain
3. **Memory & RAG**：让 AI 有记忆和知识
4. **Agent & Tools**：让 AI 自主行动
5. **生产部署**：构建完整的 AI 应用

**你现在可以开始构建自己的 AI 项目了！** 🎉

---

## 8. 学习资源

### 官方文档
- [LangChain 文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [OpenAI API 文档](https://platform.openai.com/docs/)

### 实战项目灵感
- 📝 AI 写作助手
- 📊 数据分析 Agent
- 🔍 代码审查工具
- 📚 个人知识库
- 🎯 智能任务管理

### 社区资源
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Awesome LangChain](https://github.com/kyrolabs/awesome-langchain)

---

> 🤖 **最后的 AI 助手时间**
> 
> 现在，试着让 AI 帮你设计一个属于你自己的 AI 项目：
> 
> **Prompt**: "我想做一个 [你的想法]，帮我设计技术方案，包括架构图、技术选型、关键代码示例"
> 
> 开始你的 AI 之旅吧！🚀
