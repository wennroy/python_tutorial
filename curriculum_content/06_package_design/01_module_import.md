# 第一章：Python 模块导入机制

> 🎯 **学习目标**
> - 理解 Python 模块与包的概念
> - 掌握各种导入方式及其区别
> - 理解 `__init__.py` 的作用
> - 学会处理循环导入问题

---

## 1. 引言：为什么需要模块化？

想象你在写一个大型项目，所有代码都放在一个文件里：
- 🔍 **难以查找**：5000 行代码，找个函数要翻半天
- 🔧 **难以维护**：改一个地方，担心影响其他地方
- 👥 **难以协作**：多人同时编辑同一个文件，冲突不断
- 🔄 **难以复用**：想在另一个项目用某个函数，只能复制粘贴

**模块化**就是把代码拆分成多个文件，每个文件专注做一件事。

---

## 2. 模块 vs 包：概念澄清

### 2.1 什么是模块 (Module)？

**模块就是一个 `.py` 文件**。就这么简单。

```python
# utils.py - 这就是一个模块
def greet(name):
    return f"Hello, {name}!"

PI = 3.14159
```

### 2.2 什么是包 (Package)？

**包是一个包含 `__init__.py` 的目录**，可以包含多个模块。

```
my_package/           # 这是一个包
├── __init__.py       # 必须有这个文件（Python 3.3+ 可省略，但不推荐）
├── module_a.py       # 子模块
├── module_b.py       # 子模块
└── sub_package/      # 子包
    ├── __init__.py
    └── module_c.py
```

### 2.3 `__init__.py` 的作用

`__init__.py` 有三个主要作用：

```python
# my_package/__init__.py

# 1. 标识这是一个 Python 包
# （即使是空文件也有这个作用）

# 2. 包的初始化代码
print("my_package 被导入了！")

# 3. 控制 `from package import *` 的行为
__all__ = ['module_a', 'module_b']

# 4. 提供包级别的便捷导入
from .module_a import important_function
from .module_b import ImportantClass
```

---

## 3. 导入方式详解

### 3.1 import 语句

```python
# 方式 1: 导入整个模块
import os
print(os.path.exists('/tmp'))  # 需要用 os.xxx 访问

# 方式 2: 导入模块并起别名
import numpy as np
arr = np.array([1, 2, 3])  # 用 np 代替 numpy

# 方式 3: 导入包中的模块
import my_package.module_a
my_package.module_a.some_function()  # 完整路径访问
```

### 3.2 from ... import 语句

```python
# 方式 1: 从模块导入特定对象
from os.path import exists, join
print(exists('/tmp'))  # 直接使用，不需要前缀

# 方式 2: 从模块导入所有公开对象（不推荐）
from os.path import *  # 可能导致命名冲突

# 方式 3: 导入并起别名
from collections import OrderedDict as OD
d = OD()
```

### 3.3 相对导入 vs 绝对导入

```python
# 假设项目结构：
# project/
# ├── main.py
# └── my_package/
#     ├── __init__.py
#     ├── module_a.py
#     └── utils/
#         ├── __init__.py
#         └── helper.py

# 在 module_a.py 中：

# 绝对导入（推荐）
from my_package.utils.helper import some_function

# 相对导入（包内部使用）
from .utils.helper import some_function  # 从当前包
from ..other_package import something    # 从父包（上一级）
```

> ⚠️ **注意**：相对导入只能在包内部使用，不能在直接运行的脚本中使用。

---

## 4. Python 如何找到模块？

### 4.1 模块搜索路径 (sys.path)

Python 按以下顺序查找模块：

```python
import sys
print(sys.path)

# 输出类似：
# [
#     '',                              # 1. 当前目录
#     '/usr/lib/python3.11',           # 2. 标准库
#     '/usr/lib/python3.11/site-packages',  # 3. 第三方包
#     ...
# ]
```

### 4.2 手动添加搜索路径

```python
import sys

# 方式 1: 临时添加（运行时有效）
sys.path.insert(0, '/path/to/my/modules')

# 方式 2: 使用 PYTHONPATH 环境变量
# export PYTHONPATH="/path/to/my/modules:$PYTHONPATH"
```

### 4.3 理解 `__name__` 和 `__main__`

```python
# my_module.py
def main():
    print("主程序运行")

print(f"__name__ = {__name__}")

if __name__ == "__main__":
    # 只有直接运行这个文件时才会执行
    main()
```

```bash
# 直接运行
$ python my_module.py
__name__ = __main__
主程序运行

# 作为模块导入
>>> import my_module
__name__ = my_module
# main() 不会自动执行
```

---

## 5. 常见问题与解决方案

### 5.1 循环导入 (Circular Import)

**问题**：两个模块互相导入对方

```python
# a.py
from b import func_b
def func_a():
    return "A"

# b.py
from a import func_a  # 💥 ImportError!
def func_b():
    return "B"
```

**解决方案**：

```python
# 方案 1: 延迟导入（在函数内部导入）
# a.py
def func_a():
    from b import func_b  # 需要时才导入
    return func_b()

# 方案 2: 重构代码，提取公共部分到第三个模块
# common.py
def shared_function():
    pass

# a.py
from common import shared_function

# b.py
from common import shared_function

# 方案 3: 使用 TYPE_CHECKING（仅用于类型提示）
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from b import SomeClass  # 只在类型检查时导入
```

### 5.2 ModuleNotFoundError

**问题**：找不到模块

```python
>>> import my_module
ModuleNotFoundError: No module named 'my_module'
```

**排查清单**：

```python
# 1. 检查文件是否存在
import os
print(os.path.exists('my_module.py'))

# 2. 检查是否在搜索路径中
import sys
print(sys.path)

# 3. 检查包是否有 __init__.py
# 4. 检查虚拟环境是否正确激活
# 5. 检查包名是否拼写正确（区分大小写）
```

### 5.3 ImportWarning: 导入顺序

**PEP 8 推荐的导入顺序**：

```python
# 1. 标准库
import os
import sys
from typing import List, Dict

# 2. 第三方库
import requests
import pandas as pd
from fastapi import FastAPI

# 3. 本地模块
from my_package import utils
from .helpers import format_data

# 每组之间空一行
```

---

## 6. 实用技巧

### 6.1 动态导入

```python
# 根据字符串导入模块
import importlib

module_name = "json"
json_module = importlib.import_module(module_name)
data = json_module.loads('{"key": "value"}')

# 重新加载模块（开发时有用）
importlib.reload(json_module)
```

### 6.2 检查模块是否可导入

```python
def is_module_available(module_name: str) -> bool:
    """检查模块是否可用"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

# 条件导入
if is_module_available('pandas'):
    import pandas as pd
    HAS_PANDAS = True
else:
    HAS_PANDAS = False
    print("pandas 未安装，部分功能不可用")
```

### 6.3 延迟导入优化启动时间

```python
# 不推荐：启动时全部导入
import pandas  # pandas 导入很慢！

# 推荐：需要时才导入
def process_data(data):
    import pandas as pd  # 第一次调用时才导入
    return pd.DataFrame(data)
```

---

## 7. 动手练习

### 练习 1：创建你的第一个包

```python
# 创建以下目录结构：
# my_utils/
# ├── __init__.py
# ├── string_utils.py
# └── math_utils.py

# string_utils.py
def reverse_string(s: str) -> str:
    """反转字符串"""
    return s[::-1]

# math_utils.py
def factorial(n: int) -> int:
    """计算阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# __init__.py
from .string_utils import reverse_string
from .math_utils import factorial

__all__ = ['reverse_string', 'factorial']
```

```python
# 测试你的包
from my_utils import reverse_string, factorial

print(reverse_string("hello"))  # olleh
print(factorial(5))  # 120
```

### 练习 2：解决循环导入

```python
# 修复以下循环导入问题
# user.py
from order import Order
class User:
    def create_order(self):
        return Order(self)

# order.py
from user import User  # 💥 循环导入！
class Order:
    def __init__(self, user: User):
        self.user = user
```

---

## 8. 小结

| 概念 | 说明 |
|-----|------|
| 模块 | 一个 `.py` 文件 |
| 包 | 包含 `__init__.py` 的目录 |
| `__init__.py` | 标识包、初始化代码、控制导出 |
| `sys.path` | Python 模块搜索路径 |
| `__name__` | 模块名，直接运行时为 `__main__` |
| 相对导入 | 使用 `.` 和 `..`，只能在包内使用 |
| 绝对导入 | 从项目根目录开始的完整路径 |

---

> 🤖 **AI 助手时间**
> 
> 尝试让 Copilot 帮你：
> - **Prompt**: "帮我设计一个 Python 包结构，用于管理用户认证和授权"
> - **Prompt**: "这段代码有循环导入问题，帮我重构"
