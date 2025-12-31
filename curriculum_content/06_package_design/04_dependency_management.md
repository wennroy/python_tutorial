# 第四章：依赖管理与虚拟环境

> 🎯 **学习目标**
> - 理解为什么需要虚拟环境
> - 掌握 venv、conda 等虚拟环境工具
> - 学会使用 pip、poetry、uv 管理依赖
> - 了解依赖锁定和版本冲突解决

---

## 1. 引言：依赖地狱

你可能遇到过这些问题：
- 😱 "我的电脑上能跑，你的不行？"
- 🔥 "升级了一个包，整个项目崩了"
- 🤯 "这个项目要 numpy 1.x，那个要 numpy 2.x"

这就是**依赖地狱 (Dependency Hell)**。虚拟环境和依赖管理工具就是解决方案。

---

## 2. 虚拟环境基础

### 2.1 什么是虚拟环境？

虚拟环境是一个**隔离的 Python 运行环境**，每个项目可以有自己独立的依赖包，互不干扰。

```
全局 Python 环境
├── numpy 1.26.0
├── pandas 2.1.0
└── requests 2.31.0

项目 A 虚拟环境          项目 B 虚拟环境
├── numpy 1.24.0         ├── numpy 2.0.0
├── pandas 1.5.0         ├── pandas 2.2.0
└── fastapi 0.100.0      └── django 4.2.0
```

### 2.2 使用 venv（内置工具）

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (CMD)
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate

# 验证激活成功
which python  # 应该指向 .venv 目录

# 退出虚拟环境
deactivate
```

### 2.3 使用 conda

```bash
# 创建环境
conda create -n myproject python=3.11

# 激活环境
conda activate myproject

# 列出所有环境
conda env list

# 删除环境
conda env remove -n myproject

# 导出环境
conda env export > environment.yml

# 从文件创建环境
conda env create -f environment.yml
```

### 2.4 venv vs conda 对比

| 特性 | venv | conda |
|-----|------|-------|
| 内置 | ✅ Python 自带 | ❌ 需要安装 |
| Python 版本管理 | ❌ | ✅ 可指定任意版本 |
| 非 Python 依赖 | ❌ | ✅ 支持 C 库等 |
| 速度 | 快 | 较慢 |
| 适用场景 | 纯 Python 项目 | 科学计算、数据科学 |

---

## 3. pip 包管理

### 3.1 基础命令

```bash
# 安装包
pip install requests
pip install requests==2.31.0          # 指定版本
pip install "requests>=2.28.0,<3.0"   # 版本范围
pip install requests --upgrade        # 升级到最新版

# 卸载包
pip uninstall requests

# 查看已安装的包
pip list
pip list --outdated  # 查看可升级的包

# 查看包信息
pip show requests

# 搜索包（PyPI 已禁用，用浏览器搜索）
# pip search requests  # 不再可用
```

### 3.2 requirements.txt

```bash
# 导出依赖
pip freeze > requirements.txt

# 从文件安装
pip install -r requirements.txt
```

```txt
# requirements.txt 示例
# 精确版本（推荐用于生产）
requests==2.31.0
fastapi==0.108.0
uvicorn[standard]==0.25.0

# 版本范围
pydantic>=2.0.0,<3.0.0

# 从 Git 安装
git+https://github.com/user/repo.git@v1.0.0

# 可选依赖
-e .[dev]  # 可编辑模式安装当前项目的 dev 依赖
```

### 3.3 pip 配置

```bash
# 使用国内镜像加速
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 4. 现代依赖管理工具

### 4.1 uv - 超快的包管理器

uv 是 Rust 编写的 Python 包管理器，速度比 pip 快 10-100 倍。

```bash
# 安装 uv
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 创建虚拟环境
uv venv

# 安装依赖
uv pip install requests
uv pip install -r requirements.txt

# 锁定依赖
uv pip compile requirements.in -o requirements.txt

# 同步环境
uv pip sync requirements.txt
```

### 4.2 poetry - 项目管理神器

```bash
# 安装 poetry
curl -sSL https://install.python-poetry.org | python3 -

# 创建新项目
poetry new my-project

# 在现有项目初始化
poetry init

# 添加依赖
poetry add requests
poetry add pytest --group dev  # 开发依赖

# 移除依赖
poetry remove requests

# 安装所有依赖
poetry install

# 更新依赖
poetry update

# 运行命令
poetry run python main.py
poetry run pytest
```

**pyproject.toml (Poetry)**:
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"
fastapi = "^0.108.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 4.3 pip-tools - 轻量级依赖锁定

```bash
# 安装 pip-tools
pip install pip-tools

# requirements.in - 顶层依赖（你实际需要的）
# requirements.in
fastapi
uvicorn[standard]
pydantic>=2.0

# 编译生成精确版本
pip-compile requirements.in -o requirements.txt

# 结果: requirements.txt 包含所有依赖及其传递依赖的精确版本
# fastapi==0.108.0
#     # via -r requirements.in
# pydantic==2.5.2
#     # via fastapi
# ...

# 同步环境（安装并移除多余的包）
pip-sync requirements.txt
```

---

## 5. 版本冲突解决

### 5.1 理解版本号

```
major.minor.patch
  │     │     │
  │     │     └── 修复 bug（向后兼容）
  │     └──────── 新功能（向后兼容）
  └────────────── 重大变更（可能不兼容）
```

**版本约束语法**:
```txt
==2.31.0     # 精确版本
>=2.28.0     # 最低版本
<3.0.0       # 最高版本
>=2.28.0,<3.0.0  # 范围
~=2.28.0     # 兼容版本 (>=2.28.0, <2.29.0)
^2.28.0      # Poetry: >=2.28.0, <3.0.0
```

### 5.2 诊断版本冲突

```bash
# 查看依赖树
pip install pipdeptree
pipdeptree

# 输出示例:
# fastapi==0.108.0
# ├── pydantic [required: >=1.7.4,<3.0.0, installed: 2.5.2]
# └── starlette [required: >=0.35.0,<0.36.0, installed: 0.35.1]

# 检查冲突
pipdeptree --warn fail
```

### 5.3 解决冲突策略

```python
# 问题：包 A 需要 numpy<2.0，包 B 需要 numpy>=2.0

# 策略 1: 找兼容版本
# 升级 A 或降级 B，看是否有兼容的版本组合

# 策略 2: 使用版本范围
# requirements.txt
numpy>=1.24.0,<2.0  # 找到两者都能接受的范围

# 策略 3: 放弃其中一个包
# 寻找替代品

# 策略 4: 分离环境
# 不同功能用不同虚拟环境
```

---

## 6. 最佳实践

### 6.1 项目依赖文件结构

```
my_project/
├── pyproject.toml       # 项目配置和依赖声明
├── requirements.txt     # 锁定版本（用于部署）
├── requirements-dev.txt # 开发依赖
└── requirements.in      # 顶层依赖（可选，用于 pip-tools）
```

### 6.2 依赖分层

```txt
# requirements.in - 生产依赖
fastapi
uvicorn[standard]
pydantic
sqlalchemy

# requirements-dev.in - 开发依赖
-r requirements.in
pytest
black
mypy
pre-commit
```

### 6.3 CI/CD 中的依赖安装

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests
        run: pytest
```

### 6.4 Docker 中的依赖安装

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 先复制依赖文件（利用缓存）
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 再复制代码
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 7. 常见问题

### 7.1 "pip 安装太慢"

```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用 uv（速度快 10-100 倍）
uv pip install requests
```

### 7.2 "安装包时报编译错误"

```bash
# 问题：某些包需要编译 C 扩展
# 解决方案 1: 使用预编译的 wheel
pip install --only-binary :all: numpy

# 解决方案 2: 安装编译工具
# macOS
xcode-select --install
# Ubuntu
sudo apt-get install build-essential python3-dev
# Windows
# 安装 Visual Studio Build Tools

# 解决方案 3: 使用 conda
conda install numpy  # conda 提供预编译的二进制包
```

### 7.3 "环境变量问题"

```bash
# 检查 Python 路径
which python
python --version

# 检查 pip 对应的 Python
pip --version

# 确保使用虚拟环境的 pip
python -m pip install requests  # 总是使用当前 Python 的 pip
```

---

## 8. 工具选择指南

| 场景 | 推荐工具 |
|-----|---------|
| 简单项目 | venv + pip |
| 快速安装 | uv |
| 完整项目管理 | poetry |
| 依赖锁定 | pip-tools 或 poetry |
| 数据科学 | conda |
| CI/CD | pip + requirements.txt |

---

## 9. 动手练习

### 练习 1：创建隔离的开发环境

```bash
# 1. 创建项目目录
mkdir my_web_project && cd my_web_project

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
source .venv/bin/activate  # macOS/Linux

# 4. 安装依赖
pip install fastapi uvicorn[standard] pydantic

# 5. 导出依赖
pip freeze > requirements.txt

# 6. 验证
cat requirements.txt
```

### 练习 2：解决版本冲突

```bash
# 场景：你需要同时安装这两个包，但它们有冲突
# package-a 需要 requests<2.28
# package-b 需要 requests>=2.30

# 1. 使用 pipdeptree 分析依赖
pip install pipdeptree
pipdeptree -p package-a
pipdeptree -p package-b

# 2. 找出可能的解决方案
# ...
```

---

## 10. 小结

| 工具 | 用途 | 命令 |
|-----|------|-----|
| venv | 创建虚拟环境 | `python -m venv .venv` |
| pip | 包安装 | `pip install package` |
| uv | 快速包管理 | `uv pip install package` |
| poetry | 项目管理 | `poetry add package` |
| pip-tools | 依赖锁定 | `pip-compile` |
| conda | 环境+包管理 | `conda install package` |

**关键原则**：
1. ✅ 总是使用虚拟环境
2. ✅ 锁定依赖版本
3. ✅ 分离开发和生产依赖
4. ✅ 使用 `.gitignore` 忽略虚拟环境目录

---

> 🤖 **AI 助手时间**
> 
> - **Prompt**: "帮我分析这个 requirements.txt 有什么依赖冲突"
> - **Prompt**: "帮我写一个 Dockerfile，使用多阶段构建优化 Python 应用的镜像大小"
