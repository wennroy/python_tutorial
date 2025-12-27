# Python Tutorial Platform

一个基于 AI 增强的 Python 互动教程平台。

## 🚀 快速开始

### 使用 Docker (推荐)

```bash
# 启动服务
docker-compose up -d

# 访问
# 前端: http://localhost
# API: http://localhost:8000
```

### 本地开发

**启动后端:**
```bash
cd platform_backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**启动前端:**
直接在浏览器打开 `platform_frontend/index.html`，或使用 VS Code Live Server 插件。

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
