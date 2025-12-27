# Python Tutorial Platform

一个基于 AI 增强的 Python 互动教程平台。

## 🚀 启动项目

你可以选择使用 Docker 快速启动，或者在本地手动搭建开发环境。

### 方案一：使用 Docker (推荐)

这是最简单的启动方式，不需要在本地安装 Python 环境。

1. **启动服务**
   ```bash
   docker-compose up -d
   ```

2. **访问应用**
   - 📚 **教程平台 (前端)**: [http://localhost](http://localhost)
   - 🔌 **API 文档 (后端)**: [http://localhost:8000/docs](http://localhost:8000/docs)

3. **停止服务**
   ```bash
   docker-compose down
   ```

### 方案二：本地开发 (无 Docker)

如果你需要修改平台代码或不想使用 Docker，可以手动启动。

#### 1. 启动后端 (Backend)

确保你已安装 Python 3.10+。

```bash
# 进入后端目录
cd platform_backend

# 创建并激活虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate # Windows

# 安装依赖
pip install -r requirements.txt

# 启动 API 服务
uvicorn main:app --reload --port 8000
```
后端服务将在 `http://localhost:8000` 启动。

#### 2. 启动前端 (Frontend)

前端是一个纯静态应用，但为了避免 CORS 问题，建议使用 HTTP 服务器运行，而不是直接打开文件。

**方法 A: 使用 Python 内置服务器 (推荐)**

打开一个新的终端窗口：
```bash
# 进入前端目录
cd platform_frontend

# 启动 HTTP 服务器 (端口 8080)
python -m http.server 8080
```
访问: [http://localhost:8080](http://localhost:8080)

**方法 B: 使用 VS Code Live Server**

1. 在 VS Code 中安装 "Live Server" 扩展。
2. 右键点击 `platform_frontend/index.html`。
3. 选择 "Open with Live Server"。

---

## 📁 项目结构

```
python_tutorial/
├── platform_backend/       # FastAPI 后端
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── platform_frontend/      # Vue.js 前端
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── Dockerfile
├── curriculum_content/     # 教程内容
│   ├── 00_setup/
│   └── 01_core/
├── workspace/              # 用户练习代码
├── docker-compose.yml
└── README.md
```

## 📝 如何使用

1. 在浏览器中打开教程平台
2. 在左侧导航中选择章节
3. 在 VS Code 中打开 `workspace/` 文件夹
4. 按照教程指示完成练习
5. 使用 GitHub Copilot 辅助编程

## 🤖 AI 集成

本教程深度集成 GitHub Copilot：
- 每个章节都有 "AI 助手时间" 环节
- 鼓励使用 AI 辅助完成练习
- 培养与 AI 协作的编程习惯

## 📚 教程模块

- **模块 0**: 环境搭建与 AI 工具
- **模块 1**: Python 核心数据结构
- **模块 2**: 调试技巧
- **模块 3**: 数据处理与类型系统
- **模块 4**: 编程范式
- **模块 5**: 包设计
- **模块 6**: RESTful API
- **最终项目**: 智能心情日记

## License

MIT
