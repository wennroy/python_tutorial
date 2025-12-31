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

## 5. LLM 可观测性：Langfuse 集成

在生产环境中，你需要监控和追踪每一次 LLM 调用。**Langfuse** 是一个开源的 LLM 可观测性平台。

### 5.1 为什么需要 Langfuse？

- 📊 **调用追踪**：记录每次 LLM 的输入/输出
- 💰 **成本分析**：追踪 Token 使用量和费用
- 🔍 **调试定位**：快速定位问题调用
- 📈 **性能监控**：响应时间、成功率统计
- 🏷️ **Prompt 版本管理**：管理和比较不同版本的 Prompt

### 5.2 配置 Langfuse

```python
# app/config/llm_config.py
import os

def get_langfuse_client_config() -> dict | None:
    """
    获取 Langfuse 配置（环境变量优先）
    
    Returns:
        dict(public_key=..., secret_key=..., host=...) 或 None
    """
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    if not public_key or not secret_key:
        return None
    
    return {
        "public_key": public_key,
        "secret_key": secret_key,
        "host": host
    }


def langfuse_handler(session_id: str, user_id: str, trace_name: str, metadata: dict = None):
    """
    创建 Langfuse 回调处理器
    
    Args:
        session_id: 会话 ID (用于追踪对话)
        user_id: 用户 ID
        trace_name: 追踪名称 (如 "customer_service", "code_generation")
        metadata: 额外的元数据
    
    Returns:
        CallbackHandler 或 None (如果 Langfuse 未配置)
    """
    cfg = get_langfuse_client_config()
    if not cfg:
        return None
    
    try:
        from langfuse.callback import CallbackHandler
        
        return CallbackHandler(
            **cfg,
            session_id=session_id,
            user_id=user_id,
            trace_name=trace_name,
            tags=[os.environ.get("ENV", "dev")],
            metadata=metadata or {},
            # 避免监控影响主流程
            timeout=3,
            max_retries=0,
            enabled=True,
        )
    except Exception:
        # Langfuse 是可选的，失败时静默返回 None
        return None
```

### 5.3 在 LLM 调用中使用 Langfuse

```python
# app/llm_core/base.py
from langchain_core.output_parsers.json import JsonOutputParser

class BaseLLM:
    """支持 Langfuse 追踪的 LLM 基类"""
    
    def __init__(self, tenant_id: str, task_id: str, track_name: str, 
                 message_id: str = None, extra_metadata: dict = None):
        """
        Args:
            tenant_id: 租户 ID
            task_id: 任务 ID (用作 session_id)
            track_name: 追踪名称 (如 "group_block_recognition")
            extra_metadata: 额外元数据
        """
        metadata = {'message_id': message_id}
        if extra_metadata:
            metadata.update(extra_metadata)
        
        # Langfuse handler 可能为 None
        self.langfuse_handler = langfuse_handler(
            session_id=task_id,
            user_id=tenant_id,
            trace_name=track_name,
            metadata=metadata
        )
        self.track_name = track_name
    
    async def arun(self, prompt: str) -> dict:
        """执行 LLM 调用，自动追踪到 Langfuse"""
        chain = self.model | JsonOutputParser()
        
        # 如果 Langfuse 可用，则传入 callbacks
        if self.langfuse_handler:
            response = await chain.ainvoke(
                prompt,
                config={"callbacks": [self.langfuse_handler]}
            )
        else:
            response = await chain.ainvoke(prompt)
        
        return response
```

### 5.4 构建追踪元数据

```python
# app/pipeline/utils/langfuse_metadata.py
from typing import Any, Dict, Optional

def build_langfuse_metadata(
    stage: str,
    *,
    table_id: str = None,
    table_title: str = None,
    row_count: int = None,
    column_count: int = None,
    extra: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    构建 Langfuse 追踪的元数据
    
    Args:
        stage: 处理阶段 (如 "group_recognition", "code_generation")
        table_id: 表格 ID
        table_title: 表格标题
        extra: 额外信息
    
    Returns:
        清理后的元数据字典
    """
    metadata = {
        "pipeline_stage": stage,
        "table_id": table_id,
        "table_title": table_title,
        "row_count": row_count,
        "column_count": column_count,
    }
    
    if extra:
        metadata.update(extra)
    
    # 移除空值
    return {k: v for k, v in metadata.items() if v is not None}
```

### 5.5 Langfuse Dashboard 功能

配置完成后，你可以在 Langfuse Dashboard 中：

1. **查看追踪列表**：按时间、用户、Session 筛选
2. **分析单次调用**：查看完整的输入/输出和耗时
3. **成本统计**：查看 Token 使用量和估算费用
4. **性能分析**：响应时间分布、错误率
5. **Prompt 管理**：版本控制和 A/B 测试

---

## 6. 多 Provider 支持与 Fallback 机制

生产环境中，单一 LLM Provider 可能存在故障或限制。我们需要支持多 Provider 和自动 Fallback。

### 6.1 多 Provider 配置

```python
# app/config/llm_config.py
from langchain_openai import AzureChatOpenAI, ChatOpenAI

def model(
    temperature: float = 0.2,
    request_timeout: int = 300,
    provider: str = None,
    track_name: str = None
):
    """
    获取 LLM 模型实例
    
    支持的 Provider:
    - "azure_openai": Azure OpenAI (企业级)
    - "openrouter": OpenRouter (多模型路由)
    
    Args:
        temperature: 采样温度
        request_timeout: 请求超时
        provider: 指定 Provider (可选)
        track_name: 追踪名称，用于确定模块特定配置
    """
    if provider is None:
        # 从配置或 track_name 确定 provider
        provider = get_llm_provider()
    
    if provider == "openrouter":
        return ChatOpenAI(
            model=os.environ.get("OPENROUTER_MODEL", "openai/gpt-4"),
            openai_api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            timeout=request_timeout,
        )
    elif provider == "azure_openai":
        return AzureChatOpenAI(
            azure_deployment=os.environ["AZURE_DEPLOYMENT"],
            temperature=temperature,
            timeout=request_timeout,
        )
    else:
        raise ValueError(f"不支持的 Provider: {provider}")
```

### 6.2 自动 Fallback 机制

```python
# app/llm_core/base.py
import logging

logger = logging.getLogger(__name__)

class BaseLLM:
    """支持自动 Fallback 的 LLM 基类"""
    
    async def _invoke_with_fallback(self, messages_or_prompt):
        """
        执行 LLM 调用，遇到内容过滤错误时自动切换备用模型
        
        Fallback 策略:
        1. 尝试主模型 (默认: Azure OpenAI)
        2. 如果触发内容过滤，切换到备用模型 (OpenRouter)
        3. 如果备用也失败，抛出异常
        """
        try:
            # 第一次尝试：使用主模型
            chain = await self.model() | JsonOutputParser()
            
            if self.langfuse_handler:
                response = await chain.ainvoke(
                    messages_or_prompt,
                    config={"callbacks": [self.langfuse_handler]}
                )
            else:
                response = await chain.ainvoke(messages_or_prompt)
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            
            # 检查是否是 Azure 内容过滤错误
            if "content_filter" in error_msg or "content management policy" in error_msg:
                logger.warning(
                    f"Azure 内容过滤触发，切换到备用模型 (OpenRouter)..."
                )
                
                try:
                    # 使用 OpenRouter 作为备用
                    fallback_model = model(provider="openrouter", track_name=self.track_name)
                    chain = fallback_model | JsonOutputParser()
                    
                    if self.langfuse_handler:
                        response = await chain.ainvoke(
                            messages_or_prompt,
                            config={"callbacks": [self.langfuse_handler]}
                        )
                    else:
                        response = await chain.ainvoke(messages_or_prompt)
                    
                    logger.info("使用 OpenRouter 备用模型成功")
                    return response
                    
                except Exception as fallback_error:
                    logger.error(
                        f"主模型和备用模型都失败。"
                        f"主模型错误: {error_msg}。"
                        f"备用模型错误: {fallback_error}"
                    )
                    raise e
            else:
                # 非内容过滤错误，直接抛出
                raise
```

### 6.3 模块化 LLM 配置

不同任务可能需要不同的模型：

```yaml
# config.yaml
llm_provider: azure_openai  # 默认 provider

llm_modules:
  basic_info:
    provider: azure_openai
    model_name: gpt-4.1
  
  code_generation:
    provider: openrouter
    model_name: anthropic/claude-3-opus
  
  simple_tasks:
    provider: azure_openai
    model_name: gpt-4o-mini  # 简单任务用便宜模型
```

```python
def get_module_llm_config(module_name: str) -> dict:
    """获取模块特定的 LLM 配置"""
    # 从 config.yaml 读取模块配置
    if hasattr(conf, 'llm_modules') and module_name in conf.llm_modules:
        module_config = conf.llm_modules[module_name]
        return {
            "provider": module_config.get('provider'),
            "model_name": module_config.get('model_name')
        }
    
    # 回退到默认配置
    return {
        "provider": get_llm_provider(),
        "model_name": None
    }
```

---

## 7. 生产级向量数据库：Milvus

对于大规模生产环境，Chroma 可能不够用。**Milvus** 是一个分布式向量数据库，支持百亿级向量。

### 7.1 Milvus vs Chroma 对比

| 特性 | Chroma | Milvus |
|-----|--------|--------|
| 规模 | 百万级 | 百亿级 |
| 部署 | 单机/嵌入式 | 分布式集群 |
| 标量过滤 | 基础支持 | 强大的 expr 表达式 |
| 索引类型 | HNSW | IVF_FLAT, HNSW, GPU 索引 |
| 适用场景 | 开发/小规模 | 生产/大规模 |

### 7.2 Milvus 集成实现

```python
# app/rag_core/milvus_retriever.py
from typing import List, Dict, Any, Optional
from pymilvus import (
    connections, Collection, CollectionSchema,
    FieldSchema, DataType, utility
)
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    """检索结果"""
    document: Document
    score: float
    retrieval_method: str = "milvus"


class MilvusVariableRetriever:
    """基于 Milvus 的变量检索器，支持标量字段过滤"""
    
    COLLECTION_NAME = "knowledge_base"
    VECTOR_DIM = 3072  # text-embedding-3-large 维度
    
    def __init__(self, host: str = "localhost", port: int = 19530):
        # 连接 Milvus
        connections.connect(alias="default", host=host, port=port)
        
        # 初始化 Embedding 模型
        self.embeddings_model = embeddings()
        
        # 获取或创建 Collection
        self.collection = self._get_or_create_collection()
    
    def _create_collection(self) -> Collection:
        """创建 Milvus Collection"""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.VECTOR_DIM),
            FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),  # 标量过滤字段
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=255),
        ]
        
        schema = CollectionSchema(fields=fields, description="知识库集合")
        collection = Collection(name=self.COLLECTION_NAME, schema=schema)
        
        # 创建向量索引
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index("vector", index_params)
        
        # 创建标量索引 (加速过滤)
        collection.create_index("category", {"index_type": "INVERTED"})
        
        return collection
    
    def search(
        self,
        query: str,
        category: str = None,
        top_k: int = 10,
        expr: str = None
    ) -> List[RetrievalResult]:
        """
        向量搜索 + 标量过滤
        
        Args:
            query: 查询文本
            category: 分类过滤
            top_k: 返回数量
            expr: 自定义过滤表达式 (如 'category == "macro" && type == "analysis"')
        """
        # 生成查询向量
        query_embedding = self.embeddings_model.embed_query(query)
        query_vector = [query_embedding.tolist()]
        
        # 构建过滤表达式
        if expr is None and category:
            expr = f'category == "{category}"'
        
        # 搜索参数
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        
        # 执行搜索
        results = self.collection.search(
            data=query_vector,
            anns_field="vector",
            param=search_params,
            limit=top_k,
            expr=expr,  # 标量过滤
            output_fields=["category", "content", "doc_id"]
        )
        
        # 转换结果
        retrieval_results = []
        for hit in results[0]:
            # 距离转相似度分数
            score = 1.0 / (1.0 + hit.distance)
            
            doc = Document(
                content=hit.entity.get("content", ""),
                metadata={"category": hit.entity.get("category", "")},
                doc_id=hit.entity.get("doc_id", "")
            )
            
            retrieval_results.append(RetrievalResult(document=doc, score=score))
        
        return retrieval_results
```

### 7.3 混合检索策略

```python
# app/rag_core/hybrid_retriever.py
from rank_bm25 import BM25Okapi

class HybridRetriever:
    """混合检索：向量 + BM25 关键词"""
    
    def __init__(self, milvus_retriever, documents: List[Document]):
        self.milvus_retriever = milvus_retriever
        
        # 构建 BM25 索引
        tokenized_docs = [doc.content.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        self.documents = documents
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        vector_weight: float = 0.5,
        keyword_weight: float = 0.5
    ) -> List[RetrievalResult]:
        """
        混合检索
        
        Args:
            query: 查询文本
            top_k: 返回数量
            vector_weight: 向量检索权重
            keyword_weight: 关键词检索权重
        """
        # 向量检索
        vector_results = self.milvus_retriever.search(query, top_k=top_k * 2)
        
        # BM25 关键词检索
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # 融合分数
        combined_scores = {}
        
        for result in vector_results:
            doc_id = result.document.doc_id
            combined_scores[doc_id] = {
                "document": result.document,
                "vector_score": result.score * vector_weight,
                "keyword_score": 0
            }
        
        for idx, score in enumerate(bm25_scores):
            doc_id = self.documents[idx].doc_id
            if doc_id in combined_scores:
                combined_scores[doc_id]["keyword_score"] = score * keyword_weight
            elif score > 0:
                combined_scores[doc_id] = {
                    "document": self.documents[idx],
                    "vector_score": 0,
                    "keyword_score": score * keyword_weight
                }
        
        # 计算最终分数并排序
        results = []
        for doc_id, data in combined_scores.items():
            final_score = data["vector_score"] + data["keyword_score"]
            results.append(RetrievalResult(
                document=data["document"],
                score=final_score,
                retrieval_method="hybrid"
            ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
```

---

## 8. 成本优化策略

### 8.1 Token 使用优化

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

### 8.2 调用频率控制

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

## 9. 动手挑战

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

## 10. 小结

### 本章要点
- ✅ 生产级 AI 应用的完整架构
- ✅ 安全防护：输入验证、Prompt 注入防护
- ✅ 性能优化：缓存、限流、模型选择
- ✅ **可观测性：Langfuse 集成、LLM 追踪**
- ✅ **多 Provider 支持：Azure OpenAI、OpenRouter、自动 Fallback**
- ✅ **生产级向量库：Milvus 集成、混合检索**
- ✅ 部署：Docker 化、环境配置

### 你已经学会了
通过这五章的学习，你已经掌握了：

1. **基础调用**：直接使用 LLM API
2. **LangChain 核心**：Prompt、Parser、Chain
3. **Memory & RAG**：让 AI 有记忆和知识
4. **Agent & Tools**：让 AI 自主行动
5. **生产部署**：构建完整的 AI 应用
6. **可观测性**：使用 Langfuse 追踪和监控 LLM 调用
7. **多 Provider**：支持多个 LLM 服务商和自动 Fallback
8. **生产级 RAG**：使用 Milvus 和混合检索

**你现在可以开始构建自己的 AI 项目了！** 🎉

---

## 11. 学习资源

### 官方文档
- [LangChain 文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
- [Langfuse 文档](https://langfuse.com/docs)
- [Milvus 文档](https://milvus.io/docs)

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
