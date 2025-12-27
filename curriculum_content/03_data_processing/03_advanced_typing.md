# 模块 3: 数据处理与类型系统 - 进阶类型 (Advanced Typing)

## 🎯 学习目标

完成本章后，你将能够：
- 使用 `Optional` 处理可能为 None 的值
- 使用 `Union` 处理多种可能的类型
- 使用 `Any` (并知道什么时候**不**该用它)
- 使用 `mypy` 进行静态类型检查

---

## 🪝 引言：当类型不确定时

现实世界是复杂的。
一个函数的参数可能是一个数字，也可能是一个字符串。
一个数据库查询的结果可能是一个对象，也可能是 `None`（没找到）。
基础的 `int` 和 `str` 已经不够用了。

---

## 🧠 核心概念：复杂场景的类型表达

### 1. Optional (可选类型)

如果一个变量可能是某种类型，也可能是 `None`，请使用 `Optional`。
*(Python 3.10+ 也可以写成 `int | None`)*

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None # 没找到

# 正确处理
name = find_user(999)
if name is not None:
    print(name.upper())
```

### 2. Union (联合类型)

如果一个变量可能是 A 类型，也可能是 B 类型。
*(Python 3.10+ 推荐使用 `|` 符号)*

```python
from typing import Union

# 旧写法
def process(data: Union[int, str]) -> None:
    pass

# 新写法 (Python 3.10+)
def process_new(data: int | str) -> None:
    if isinstance(data, int):
        print(f"Number: {data}")
    else:
        print(f"String: {data}")
```

### 3. Any (任意类型)

`Any` 是类型系统的"逃生门"。当你标记一个变量为 `Any` 时，你告诉类型检查器："别管这个，我心里有数（或者我懒得写）"。

```python
from typing import Any

def magic_box(item: Any) -> Any:
    return item
```

> ⚠️ **警告**：滥用 `Any` 会让类型检查形同虚设。尽量避免使用它，除非你真的无法确定类型。

---

## 🛡️ 静态检查工具：mypy

IDE 的提示虽然好，但不够严格。`mypy` 是 Python 官方推荐的静态类型检查工具。它可以像编译器一样扫描你的代码，找出类型错误。

**安装**: `pip install mypy`

**使用**:
```bash
mypy script.py
```

如果你的代码写着 `a: int = "hello"`, mypy 会报错：
`error: Incompatible types in assignment (expression has type "str", variable has type "int")`

---

## 🤖 AI 助手时间

> **Prompt**: "解释 Python 中的 `Callable` 类型注解是什么？请举一个例子，说明如何注解一个接收回调函数作为参数的函数。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 函数也可以作为参数传递，这时候怎么写类型注解呢？

---

## ✅ 动手挑战

继续完善 `exercise_03_02.py`，或者创建一个新文件。

**任务**：
1. 定义一个函数 `safe_divide(a, b)`，它接收两个数字（int 或 float），返回除法结果。如果分母为 0，返回 `None`。
2. 使用 `Union` (或 `|`) 和 `Optional` 为其添加完美的类型注解。
3. 运行 `mypy` 检查你的代码。

---

## 📝 总结

- **Optional[T]** = `T | None`。
- **Union[A, B]** = `A | B`。
- **Any** 是放弃治疗，慎用。
- **mypy** 是你的代码质量守门员，建议集成到 CI/CD 流程中。

下一章：办公自动化——让 Python 帮你写报告！
