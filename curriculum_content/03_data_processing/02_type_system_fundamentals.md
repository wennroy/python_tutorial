# 模块 3: 数据处理与类型系统 - 类型系统基础 (Type Hinting)

## 🎯 学习目标

完成本章后，你将能够：
- 理解**动态类型**与**静态类型**的区别
- 掌握 Python 的**类型注解 (Type Hints)** 语法
- 使用 `list[]`, `dict[]` 等泛型别名 (Python 3.9+)
- 体验 IDE 带来的智能提示增强

---

## 🪝 引言：鸭子类型与文档噩梦

Python 是动态语言，崇尚"鸭子类型" (Duck Typing)："如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子"。
这写起来很爽，但维护起来很火葬场。
当你接手别人的代码，看到 `def process(data):` 时，你一定会问：`data` 到底是什么？是字典？列表？还是对象？

**Type Hints** 就是为了解决这个问题而生的——它不影响代码运行，但能让代码变得"可读"且"可查"。

---

## 🧠 核心概念：给变量贴标签

### 1. 变量注解

```python
# 以前的写法
name = "Alice"
age = 30

# 加上类型注解
name: str = "Alice"
age: int = 30
is_active: bool = True
```

### 2. 函数注解 (最重要！)

这是类型注解收益最大的地方。

```python
def greeting(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b
```

现在，当你调用 `add("1", "2")` 时，虽然 Python 解释器不会报错（它会返回 "12"），但 IDE（VS Code/PyCharm）会给你画红线警告：`Expected type 'int', got 'str' instead`。

### 3. 容器类型 (List, Dict)

在 Python 3.9 之前，你需要 `from typing import List, Dict`。
在 Python 3.9+，你可以直接使用内置类型：

```python
# 列表：包含整数的列表
scores: list[int] = [90, 80, 95]

# 字典：Key是字符串，Value是浮点数
prices: dict[str, float] = {"apple": 1.5, "banana": 2.0}

# 混合嵌套
users: list[dict[str, str]] = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]
```

---

## 🤖 AI 助手时间

> **Prompt**: "我有以下遗留代码，没有任何类型注解。请帮我添加 Python 3.10+ 风格的 Type Hints，并添加 Google 风格的 Docstring。"
> 
> ```python
> def calculate_stats(numbers, normalize=False):
>     if normalize:
>         avg = sum(numbers) / len(numbers)
>         return [n - avg for n in numbers]
>     return sum(numbers)
> ```
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 注意 AI 是如何处理 `numbers` (可能是 list) 和返回值 (可能是 list 或 float) 的？它可能会用到 `Union`。

---

## ✅ 动手挑战

我们将使用 `exercise_03_02.py`。

**任务**：
1. 这是一个没有任何类型注解的脚本。
2. 为所有变量和函数添加正确的类型注解。
3. 尝试传入错误的类型（例如给需要 int 的函数传 str），观察 IDE 的反应。

---

## 📝 总结

- 类型注解是**给人和 IDE 看的**，Python 解释器会忽略它。
- 它可以极大地提升代码的**可维护性**和 IDE 的**自动补全**能力。
- 从 Python 3.9 开始，优先使用内置的 `list`, `dict`, `tuple` 而不是 `typing` 模块的大写版本。

下一章：进阶类型——处理更复杂的情况！
