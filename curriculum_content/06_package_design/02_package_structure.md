# 第二章：Python 包结构设计

> 🎯 **学习目标**
> - 掌握专业 Python 项目的目录结构
> - 学会使用 `setup.py` / `pyproject.toml` 配置包
> - 理解版本管理和发布流程
> - 了解开源项目的最佳实践

---

## 1. 引言：为什么包结构很重要？

一个好的包结构就像一个整洁的房间：
- 📁 **东西好找**：新成员能快速定位代码
- 🔧 **易于维护**：修改一处不影响其他
- 📦 **便于分发**：一条命令就能安装
- ✅ **便于测试**：测试代码与业务代码分离

---

## 2. 标准项目结构

### 2.1 基础结构（小型项目）

```
my_project/
├── my_package/           # 源代码目录（包名）
│   ├── __init__.py       # 包初始化
│   ├── core.py           # 核心逻辑
│   └── utils.py          # 工具函数
├── tests/                # 测试目录
│   ├── __init__.py
│   └── test_core.py
├── README.md             # 项目说明
├── requirements.txt      # 依赖列表
└── setup.py              # 安装配置（或 pyproject.toml）
```

### 2.2 完整结构（生产项目）

```
my_project/
├── src/                  # 源代码根目录（src layout）
│   └── my_package/
│       ├── __init__.py
│       ├── __main__.py   # 允许 python -m my_package
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── services.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── config.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # pytest 配置
│   ├── unit/
│   │   └── test_models.py
│   └── integration/
│       └── test_api.py
├── docs/                 # 文档
│   ├── index.md
│   └── api.md
├── scripts/              # 脚本工具
│   └── setup_db.py
├── .github/              # GitHub 相关
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .env.example          # 环境变量模板
├── README.md
├── LICENSE
├── pyproject.toml        # 现代 Python 项目配置
├── setup.py              # 兼容旧工具（可选）
└── Makefile              # 常用命令快捷方式
```

### 2.3 src Layout vs Flat Layout

**Flat Layout（传统）**：
```
my_project/
├── my_package/        # 包直接在根目录
│   └── __init__.py
└── tests/
```

**src Layout（推荐）**：
```
my_project/
├── src/
│   └── my_package/    # 包在 src 目录下
│       └── __init__.py
└── tests/
```

**为什么推荐 src Layout？**
- 防止意外导入本地未安装的包
- 测试时更接近真实安装环境
- 避免与项目根目录下的同名模块冲突

---

## 3. 关键文件详解

### 3.1 `__init__.py` - 包的入口

```python
# src/my_package/__init__.py

# 版本信息
__version__ = "0.1.0"
__author__ = "Your Name"

# 导出公开 API
from .core.models import User, Order
from .core.services import create_user, process_order

# 控制 `from my_package import *` 的行为
__all__ = [
    "User",
    "Order", 
    "create_user",
    "process_order",
]

# 包初始化逻辑（可选）
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
```

### 3.2 `__main__.py` - 命令行入口

```python
# src/my_package/__main__.py
"""
允许通过 `python -m my_package` 运行
"""
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
```

### 3.3 `pyproject.toml` - 现代项目配置

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "一个示例 Python 包"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your@email.com"}
]
requires-python = ">=3.9"

# 运行时依赖
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
]

# 可选依赖
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
docs = [
    "mkdocs>=1.4.0",
    "mkdocs-material>=9.0.0",
]

# 命令行入口点
[project.scripts]
my-cli = "my_package.cli:main"

# 项目 URL
[project.urls]
Homepage = "https://github.com/username/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/username/my-package"

# setuptools 配置
[tool.setuptools.packages.find]
where = ["src"]

# pytest 配置
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

# black 配置
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']

# mypy 配置
[tool.mypy]
python_version = "3.11"
strict = true
```

### 3.4 `setup.py` - 兼容旧工具

```python
# setup.py（如果需要兼容旧工具）
from setuptools import setup

# 配置已在 pyproject.toml 中，这里只是兼容层
setup()
```

---

## 4. 依赖管理

### 4.1 requirements.txt vs pyproject.toml

| 文件 | 用途 | 示例 |
|-----|------|-----|
| `requirements.txt` | 精确锁定版本（部署用） | `requests==2.31.0` |
| `pyproject.toml` | 指定兼容范围（开发用） | `requests>=2.28.0` |

```bash
# requirements.txt - 精确版本
requests==2.31.0
pydantic==2.5.2
fastapi==0.108.0
uvicorn[standard]==0.25.0

# 生成 requirements.txt
pip freeze > requirements.txt
```

### 4.2 开发依赖分离

```bash
# 安装基础依赖
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"

# 安装所有可选依赖
pip install -e ".[dev,docs]"
```

### 4.3 使用 pip-tools 管理依赖

```bash
# 安装 pip-tools
pip install pip-tools

# requirements.in - 顶层依赖
requests>=2.28.0
fastapi>=0.100.0

# 编译精确版本
pip-compile requirements.in -o requirements.txt

# 同步环境
pip-sync requirements.txt
```

---

## 5. 版本管理

### 5.1 语义化版本 (Semantic Versioning)

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── 向后兼容的 bug 修复
  │     └──────── 向后兼容的新功能
  └────────────── 不兼容的 API 变更
```

示例：
- `1.0.0` → `1.0.1`：修复 bug
- `1.0.0` → `1.1.0`：添加新功能
- `1.0.0` → `2.0.0`：重大变更，可能不兼容

### 5.2 版本号在代码中的位置

```python
# 方式 1: __init__.py 中定义
# src/my_package/__init__.py
__version__ = "0.1.0"

# 方式 2: 单独的 _version.py
# src/my_package/_version.py
__version__ = "0.1.0"

# __init__.py
from ._version import __version__

# 方式 3: 使用 importlib.metadata（推荐）
# src/my_package/__init__.py
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("my-package")
except PackageNotFoundError:
    __version__ = "unknown"
```

---

## 6. 发布到 PyPI

### 6.1 发布前检查清单

```markdown
- [ ] 更新版本号
- [ ] 更新 CHANGELOG
- [ ] 所有测试通过
- [ ] 代码格式化完成
- [ ] README 更新
- [ ] 清理构建文件
```

### 6.2 构建和发布

```bash
# 安装构建工具
pip install build twine

# 清理旧构建
rm -rf dist/ build/ *.egg-info

# 构建包
python -m build

# 检查包
twine check dist/*

# 上传到 TestPyPI（测试）
twine upload --repository testpypi dist/*

# 上传到 PyPI（正式）
twine upload dist/*
```

### 6.3 GitHub Actions 自动发布

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

---

## 7. 最佳实践

### 7.1 代码组织原则

```python
# ✅ 好的组织：按功能分模块
my_package/
├── auth/           # 认证相关
│   ├── login.py
│   └── token.py
├── users/          # 用户相关
│   ├── models.py
│   └── services.py
└── utils/          # 通用工具

# ❌ 差的组织：按类型分模块
my_package/
├── models/         # 所有 models
│   ├── user.py
│   ├── order.py
│   └── product.py
├── services/       # 所有 services
│   ├── user.py
│   └── order.py
```

### 7.2 导出控制

```python
# src/my_package/__init__.py

# 明确导出公开 API
from .core import create_user, get_user
from .models import User

__all__ = ["create_user", "get_user", "User"]

# 内部模块使用下划线前缀
# src/my_package/_internal.py  # 约定为内部使用
```

### 7.3 配置文件模板

```python
# src/my_package/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    app_name: str = "My App"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 8. 动手练习

### 练习：创建一个完整的 Python 包

```bash
# 1. 创建项目结构
mkdir -p my_calculator/src/calculator/tests
cd my_calculator

# 2. 创建必要文件
touch src/calculator/__init__.py
touch src/calculator/core.py
touch tests/__init__.py
touch tests/test_core.py
touch pyproject.toml
touch README.md
```

```python
# src/calculator/__init__.py
__version__ = "0.1.0"
from .core import add, subtract, multiply, divide
__all__ = ["add", "subtract", "multiply", "divide"]

# src/calculator/core.py
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```toml
# pyproject.toml
[project]
name = "my-calculator"
version = "0.1.0"
description = "A simple calculator package"
requires-python = ">=3.9"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

```bash
# 3. 安装并测试
pip install -e .
python -c "from calculator import add; print(add(1, 2))"
```

---

## 9. 小结

| 组件 | 作用 |
|-----|------|
| `src/` | 源代码目录，隔离开发与安装环境 |
| `__init__.py` | 包初始化，定义公开 API |
| `__main__.py` | 命令行入口 |
| `pyproject.toml` | 现代项目配置标准 |
| `requirements.txt` | 精确依赖锁定 |
| `tests/` | 测试代码目录 |

---

> 🤖 **AI 助手时间**
> 
> - **Prompt**: "帮我生成一个 Python 包的 pyproject.toml，支持 FastAPI 和 pytest"
> - **Prompt**: "这个项目结构有什么问题？帮我优化"
