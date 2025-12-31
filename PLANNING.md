# Python AI 增强互动教程平台项目计划

## 1. 项目概览
**项目目标**: 构建一个 **Web 教学平台**，用于托管和展示一套高质量的 Python 互动教程。
**核心内容**: 教程内容分为“Python 基础进阶”与“实战项目：智能心情日记”两大部分。
**平台特色**: 寓教于乐，非枯燥文字，结合 AI (GitHub Copilot) 辅助学习。
**部署目标**: 最终部署在用户私有服务器上。

## 2. 技术栈 (Tech Stack)

### 2.1 教学平台本身 (The Platform)
*这是为了实现“教程展示”所使用的技术栈*
*   **后端 (Backend)**: Python (FastAPI) - 提供 API，处理教案解析与分发。
*   **前端 (Frontend)**: React 或 Vue.js (推荐) - 构建响应式、交互性强的学习界面。
*   **内容渲染 (Content Engine)**:
    *   `markdown`: 解析 Markdown 章节。
    *   `nbconvert`: 将 Jupyter Notebook 转换为 HTML 用于网页展示。
*   **部署 (Deployment)**: Docker & Nginx (用于服务器托管)。

### 2.2 教程教授的技术栈 (The Curriculum Stack)
*这是学生在教程中将要学习和使用的技术栈*
*   **语言**: Python 3.10+
*   **Web 框架**: FastAPI
*   **数据库**: SQLite
*   **数据分析**: Pandas
*   **AI 工具**: GitHub Copilot
*   **测试**: Pytest

## 3. 平台技术架构方案 (Technical Architecture)

### 3.1 前端设计 (Frontend Design)
*   **布局**: 左侧为可折叠的课程目录树 (Sidebar)，右侧为沉浸式阅读/交互区域 (Main Content)。
*   **交互**:
    *   **代码高亮**: 使用 `Prism.js` 或 `Highlight.js` 美化代码块。
    *   **进度追踪**: 本地存储 (LocalStorage) 记录用户的阅读进度。
    *   **实时代码同步**: 前端通过 WebSocket 或轮询机制，实时展示用户在 VS Code 中编辑的代码文件的最新状态（只读展示或 Diff 对比）。

### 3.2 后端设计 (Backend Design)
*   **API 接口**:
    *   `GET /api/curriculum`: 返回完整的课程目录结构 (JSON)。
    *   `GET /api/chapter/{id}`: 读取指定章节文件，动态渲染为 HTML 返回。
    *   `GET /api/code/{filename}`: 读取用户工作区中特定 Python 文件的内容。
*   **文件读取机制**:
    *   后端维护一个 `content/` 目录，映射文件系统路径。
    *   **Markdown 处理**: 读取 `.md` -> 使用 `markdown` 库转 HTML -> 注入 CSS 样式。
    *   **Notebook 处理**: 读取 `.ipynb` -> 使用 `nbconvert.HTMLExporter` 转 HTML -> 移除多余的 Jupyter 样式以适配网页。

### 3.3 交互模式 (Interaction Model)
*   **本地运行**: 用户在 VS Code 中启动 FastAPI 服务。
*   **双屏体验**: 浏览器展示教程与代码 Diff，VS Code 进行实际编码与 Copilot 交互。
*   **文件命名规范**:
    为了确保后端能正确读取并展示用户正在编辑的代码，教程中的练习文件将遵循严格的命名约定：
    *   `exercise_{module_id}_{step}.py` (例如: `exercise_01_01.py`)
    *   后端将根据当前章节元数据，自动寻找对应的 `exercise_*.py` 文件并展示在前端。

## 4. 教学内容设计规范 (Instructional Design Guidelines)
*本指南用于规范每一章节的撰写风格与结构，确保教程的一致性与高质量，并指导 AI 生成内容。*

### 4.1 章节标准结构 (Standard Chapter Structure)
每个教学模块（Notebook 或 Markdown）应遵循以下结构：

1.  **引言 (The Hook)**:
    *   用一个生活中的例子或实际问题引入本章主题。
    *   明确本章的学习目标 (Learning Objectives)。
2.  **核心概念 (The Concept)**:
    *   图文并茂地解释技术原理（避免大段枯燥文字）。
    *   使用类比 (Analogy) 帮助理解（例如：变量是盒子，函数是机器）。
3.  **代码实战 (Code in Action)**:
    *   提供可运行的代码示例。
    *   **关键点**: 代码必须简洁，变量命名要有意义。
4.  **AI 结对编程 (Pair Programming with AI)**:
    *   **核心环节**: 设计具体的场景，引导学生使用 Copilot。
    *   *Example*: "现在，试着在注释里写 `# 生成一个计算斐波那契数列的函数`，看看 Copilot 会给你什么建议。"
    *   分析 AI 生成的代码，指出其优缺点。
5.  **动手挑战 (Hands-on Challenge)**:
    *   布置一个小作业，要求学生独立或在 AI 辅助下完成。
6.  **总结与延伸 (Summary & Next Steps)**:
    *   回顾本章重点。
    *   预告下一章内容。

### 4.2 写作风格 (Tone & Style)
*   **对话式**: 像坐在学生旁边的学长一样说话，多用“我们”、“试一试”。
*   **鼓励性**: 对难点进行心理建设，庆祝每一个小的成功。
*   **实用主义**: 始终强调“为什么要学这个”以及“它在实际项目中怎么用”。

### 4.3 AI 交互设计 (AI Interaction Design)
在教程中，必须显式地包含 AI 交互指令块：
> 🤖 **AI 助手时间**:
> *   **Prompt**: "解释这段代码中的 `yield` 关键字的作用"
> *   **Action**: 选中代码，使用 `Cmd+I` (macOS) 或 `Ctrl+I` (Windows) 唤起 Copilot Chat。
> *   **Reflection**: AI 的解释清楚吗？它有没有漏掉什么？

## 6. 建议的项目结构 (Project Structure)

### 第一阶段：Python 核心与进阶 (Python Mastery)

#### 模块 0: 现代化环境搭建
*   VS Code, Python 环境, 虚拟环境。
*   **AI 聚焦**: Copilot 安装与基础指令。

#### 模块 1: Python 核心强化
*   List/Dict/Set 深度解析与底层原理。
*   内存管理、引用、深浅拷贝 (`copy` 模块)。
*   **AI 聚焦**: 用 Copilot 可视化内存引用。

#### 模块 2: 调试艺术与工具使用 (The Art of Debugging)
*   **IDE 调试基础**:
    *   **VS Code**: `launch.json` 配置, 断点 (Breakpoints), 变量监视 (Watch), 调用堆栈 (Call Stack)。
    *   **PyCharm**: 调试配置, 智能步进 (Smart Step Into), 表达式求值 (Evaluate Expression)。
*   **跨平台操作指南**:
    *   **Windows vs macOS**: 快捷键差异 (F5/F10/F11 vs Cmd+Shift+...), 路径处理差异。
*   **高级调试技巧**:
    *   条件断点 (Conditional Breakpoints)。
    *   日志调试 (Logpoints) - 不修改代码打印日志。
    *   调试崩溃与异常 (Exception Breakpoints)。
*   **AI 聚焦**: 让 Copilot 解释报错堆栈 (Traceback), 自动修复简单的逻辑错误。

#### 模块 3: 数据处理与类型系统
*   **文件读写**: JSON, CSV, Excel (`pandas`), Word (`python-docx`)。
*   **Type Hinting**: 基础注解, `Optional`, `Union`, `Generic`, `mypy` 静态检查。
*   **AI 聚焦**: 自动生成 Type Hint 和文档字符串。

#### 模块 4: 编程范式对比
*   OOP (面向对象) vs FP (面向函数)。
*   类、继承、多态 vs 纯函数、高阶函数、Lambda。
*   **AI 聚焦**: 代码范式重构 (OOP -> FP)。

#### 模块 5: AI 开发实战 (AI Development)
*   **第一章: AI 开发全景图**
    *   当前 AI 开发生态的核心组件
    *   LLM 基本调用方式 (OpenAI, Anthropic, 本地模型)
    *   环境搭建与 API Key 配置
*   **第二章: LangChain 核心概念**
    *   Prompt Templates (提示模板设计)
    *   Output Parsers (结构化输出)
    *   LCEL 表达式语言 (链式调用)
*   **第三章: Memory 与 RAG**
    *   对话记忆实现
    *   向量嵌入与向量数据库 (Chroma)
    *   检索增强生成 (RAG) 完整流程
*   **第四章: Agent 与工具调用**
    *   Agent 工作原理 (ReAct 模式)
    *   自定义工具开发
    *   LangGraph 状态图构建
    *   Human-in-the-Loop 人机协作
*   **第五章: AI 应用实战**
    *   生产级项目架构设计
    *   安全防护 (Prompt 注入防护)
    *   性能优化与成本控制
    *   部署与监控
*   **AI 聚焦**: 构建完整的 AI 应用，从 Demo 到生产

#### 模块 6: 包设计与生态
*   **第一章: 模块导入机制** - `__init__.py`, 相对导入 vs 绝对导入, sys.path
*   **第二章: Package 结构设计** - src layout, pyproject.toml, 发布到 PyPI
*   **第三章: requests 与 HTTP** - HTTP 基础, requests 库, Session 管理
*   **第四章: 依赖管理** - venv, pip, uv, poetry, 版本冲突解决
*   **AI 聚焦**: 让 Copilot 生成项目结构和配置文件

#### 模块 7: RESTful API 设计与网络基础 (RESTful API Foundations) (待开发)
*   **HTTP 协议核心**: 请求方法 (GET, POST, PUT, DELETE), 状态码 (2xx, 4xx, 5xx), Header 与 Body。
*   **REST 架构风格**: 资源 (Resources), 表现层 (Representation), 状态转移 (State Transfer)。
*   **API 设计规范**: URL 命名规则, JSON 数据格式, 幂等性 (Idempotency)。
*   **FastAPI 初探**: 快速搭建一个简单的 API 端点, 理解 Path Parameters 与 Query Parameters。
*   **AI 聚焦**: 让 Copilot 解释 HTTP 状态码含义, 生成符合 REST 规范的 API 接口定义 (OpenAPI/Swagger)。

#### 模块 Special: 算法实战 (LeetCode)
*   精选题目 (Two Sum 等)。
*   Pythonic 解法与复杂度分析。

#### 模块 Extra: 常用模块拓展 (可选)
*   `asyncio` (并发), `logging` (日志), `argparse` (CLI), `re` (正则), `datetime`。
*   **Docker 基础**: Windows/macOS/Linux 安装指南与基础使用。
*   **Git 版本控制**: 基础工作流与修改提交历史（修改 Author/Email）。

### 第二阶段：终极实战项目 (Capstone Project)

#### 模块 Final: 打造“智能心情日记” (Smart Journal)
*这是一个综合性的大模块，将之前学到的所有知识串联起来*
1.  **后端架构 (Backend Core)**:
    *   使用 FastAPI 搭建 RESTful API。
    *   设计 Pydantic 模型 (Data Validation)。
2.  **数据持久化 (Database)**:
    *   集成 SQLite。
    *   实现 CRUD 操作 (增删改查日记)。
3.  **前端交互 (Frontend Integration)**:
    *   构建简单的 HTML/JS 界面。
    *   使用 `fetch` 对接后端 API。

### 当前实际项目结构 (Current Project Structure)

```
python_tutorial/
├── docker-compose.dev.yml
├── docker-compose.yml
├── PLANNING.md
├── README.md
├── curriculum_content/         # [教案] 实际的教程文件
│   ├── 00_setup/               # 模块 0: 现代化环境搭建
│   │   ├── 01_python_installation.md
│   │   ├── 02_virtual_environments.md
│   │   ├── 03_ide_setup.md
│   │   ├── 04_first_steps.md
│   │   ├── 05_proxy_configuration.md
│   │   └── solutions/
│   ├── 01_core/                # 模块 1: Python 核心强化
│   │   ├── 01_list_deep_dive.md
│   │   ├── 02_dict_set_under_the_hood.md
│   │   ├── 03_memory_management.md
│   │   ├── 04_string_text_processing.md
│   │   ├── 05_file_io_context_managers.md
│   │   ├── 06_datetime_handling.md
│   │   └── solutions/
│   ├── 02_debugging/           # 模块 2: 调试艺术与工具使用
│   │   ├── 01_vscode_debugger.md
│   │   ├── 02_advanced_techniques.md
│   │   ├── 03_ai_assisted_debugging.md
│   │   ├── 04_pycharm_debugger.md
│   │   ├── 05_ide_productivity_hacks.md
│   │   └── solutions/
│   ├── 03_data_processing/     # 模块 3: 数据处理与类型系统
│   │   ├── 01_pandas_basics.md
│   │   ├── 02_type_system_fundamentals.md
│   │   ├── 03_advanced_typing.md
│   │   ├── 04_office_automation.md
│   │   ├── 05_file_encoding.md
│   │   └── solutions/
│   ├── 04_paradigms/           # 模块 4: 编程范式对比
│   │   ├── 01_oop_concepts.md
│   │   ├── 02_advanced_oop.md
│   │   ├── 03_functional_concepts.md
│   │   ├── 04_oop_vs_fp_refactoring.md
│   │   ├── 05_design_patterns_practice.md
│   │   └── solutions/
│   ├── 05_ai_development/       # 模块 5: AI 开发实战 (新增)
│   │   ├── 01_ai_landscape.md           # AI 开发全景图
│   │   ├── 02_langchain_core.md         # LangChain 核心概念
│   │   ├── 03_memory_and_rag.md         # Memory 与 RAG
│   │   ├── 04_agents_and_tools.md       # Agent 与工具调用
│   │   ├── 05_production_project.md     # AI 应用实战
│   │   └── solutions/
│   ├── 06_package_design/       # 模块 6: 包设计与生态 (新增)
│   │   ├── 01_module_import.md          # 模块导入机制
│   │   ├── 02_package_structure.md      # Package 结构设计
│   │   ├── 03_requests_http.md          # requests 与 HTTP
│   │   ├── 04_dependency_management.md  # 依赖管理
│   │   └── solutions/
│   └── 99_extra/               # 模块 Extra: 常用模块拓展
│       ├── 01_visualization_basics.md
│       ├── 02_streamlit_dashboard.md
│       ├── 03_logging_mastery.md
│       ├── 04_docker_installation.md
│       ├── 05_git_version_control.md
│       └── solutions/
├── platform_backend/           # [平台] 后端代码 (FastAPI)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── platform_frontend/          # [平台] 前端代码
│   ├── app.js
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   └── style.css
└── workspace/                  # 用户练习工作区
    ├── exercise_00_01.py
    └── exercise_01_01.py
```

## 7. 下一步计划
1.  确认此技术架构方案。
2.  初始化 `platform_backend` 和 `curriculum_content` 目录。
3.  编写第一个教案文件作为测试。
4.  实现后端的内容解析引擎。

## 8. AI 开发模块增强需求 (参考 atlas_tfl_ai 项目)

### 8.1 需要补充的生产级 AI 技术

基于 `atlas_tfl_ai` 项目的实际应用，需要在 `05_ai_development` 模块中补充以下内容：

#### 8.1.1 Langfuse - LLM 可观测性平台
- **用途**: LLM 调用追踪、性能监控、成本分析
- **核心功能**:
  - 追踪每次 LLM 调用的输入/输出
  - Session 级别的对话追踪
  - Token 使用量和成本统计
  - Prompt 模板管理和版本控制
- **实现方式**: 通过 `CallbackHandler` 集成到 LangChain

#### 8.1.2 Milvus - 向量数据库
- **用途**: 大规模向量存储和相似性检索
- **核心功能**:
  - 高性能向量索引 (IVF_FLAT, HNSW 等)
  - 标量字段过滤 (expr 表达式)
  - 分布式架构支持
  - 支持混合检索 (向量 + 关键词)
- **对比 Chroma**: 适合更大规模的生产环境

#### 8.1.3 多 LLM Provider 支持
- **支持的 Provider**:
  - Azure OpenAI (企业级)
  - OpenRouter (多模型路由)
  - 本地模型
- **Fallback 机制**: 当主模型触发内容过滤时自动切换备用模型
- **模块化配置**: 不同任务使用不同模型

#### 8.1.4 高级 RAG 架构
- **混合检索策略**:
  - Dense Retrieval (向量相似性)
  - Sparse Retrieval (BM25 关键词匹配)
  - Hybrid Retrieval (加权融合)
- **Reranking**: 对初步结果进行重排序
- **多知识库管理**: Global KB + Project-level KB

#### 8.1.5 生产级异步处理
- **技术栈**:
  - `aiohttp` / `aiofiles` 异步 I/O
  - `gevent` / `greenlet` 协程支持
  - Redis 缓存和消息队列
  - Kafka 消息队列 (高吞吐场景)

### 8.2 待更新的文件

| 文件 | 需要补充的内容 |
|------|---------------|
| `05_production_project.md` | Langfuse 集成、Milvus 使用、多 Provider 支持、Fallback 机制 |
| `03_memory_and_rag.md` | 高级 RAG 架构、Milvus 向量库、混合检索策略 |
| `01_ai_landscape.md` | 可观测性工具 (Langfuse/LangSmith)、向量数据库对比 |
