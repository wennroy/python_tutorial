# 模块 1: Python 核心强化 - 文件 IO 与上下文管理器

## 🎯 学习目标

完成本章后，你将能够：
- 熟练进行文件读写操作 (`open`, `read`, `write`)
- 深刻理解上下文管理器 (`with` 语句) 的作用
- 掌握 `pathlib` 这一现代路径处理库
- 学会处理 JSON 和 CSV 文件

---

## 🪝 引言：忘记关闭文件的代价

你写了一个程序，运行了一天后突然崩溃了，报错说 "Too many open files"。
或者你写完文件后打开一看，里面是空的，因为数据还在缓冲区里没刷入磁盘。

这都是因为没有正确关闭文件资源。在 Python 中，我们有一个优雅的解决方案：`with` 语句。

---

## 🧠 核心概念：上下文管理器 (Context Manager)

### 1. 传统的 try-finally 写法（不推荐）

```python
f = open("data.txt", "w")
try:
    f.write("Hello")
finally:
    f.close() # 必须手动关闭，否则资源泄漏
```

### 2. 优雅的 `with` 写法（推荐）

```python
# 离开缩进块时，文件会自动关闭，即使发生了异常！
with open("data.txt", "w") as f:
    f.write("Hello World")
```

任何实现了 `__enter__` 和 `__exit__` 方法的对象都可以用于 `with` 语句。这不仅限于文件，还可以用于数据库连接、锁 (Lock) 等。

---

## 📂 现代路径处理：pathlib

忘掉 `os.path.join` 吧，`pathlib` 才是面向对象的未来。

```python
from pathlib import Path

# 创建路径对象
p = Path("data_folder") / "sub_folder" / "file.txt"

# 检查是否存在
if not p.parent.exists():
    p.parent.mkdir(parents=True) # 自动创建父目录

# 写入文本
p.write_text("Content", encoding="utf-8")

# 读取文本
content = p.read_text(encoding="utf-8")

# 遍历目录
for file in Path(".").glob("*.py"):
    print(file.name)
```

---

## 💾 常见数据格式：JSON 与 CSV

Python 内置了强大的库来处理这两种格式。

### JSON (JavaScript Object Notation)
```python
import json

data = {"name": "Alice", "skills": ["Python", "SQL"]}

# 序列化 (Dump): Python -> JSON String
json_str = json.dumps(data, indent=2)

# 反序列化 (Load): JSON String -> Python
obj = json.loads(json_str)

# 读写文件
with open("data.json", "w") as f:
    json.dump(data, f)
```

### CSV (Comma-Separated Values)
```python
import csv

# 写入
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", 30])

# 读取
with open("data.csv", "r") as f:
    reader = csv.DictReader(f) # 读成字典，更直观
    for row in reader:
        print(row["Name"], row["Age"])
```

---

## 🤖 AI 助手时间

> **Prompt**: "解释 Python 中 `with` 语句背后的 `__enter__` 和 `__exit__` 魔术方法是如何工作的？并帮我写一个计算代码块执行时间的自定义 Context Manager。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 看看 AI 生成的 `Timer` 类，尝试理解 `__exit__` 中的参数 (`exc_type`, `exc_val`, `exc_tb`) 是做什么的。

---

## ✅ 动手挑战

创建文件 `exercise_01_05.py`，完成以下任务：

```python
# 1. 目录扫描器
#    使用 pathlib 扫描当前目录下所有的 .py 文件。
#    统计每个文件的行数，并输出一个报告：
#    filename | lines
#    main.py  | 120
#    ...

# 2. JSON 转换器
#    读取一个 CSV 文件（自己创建一个简单的），将其转换为 JSON 格式并保存。
#    CSV:
#    id,name,score
#    1,Alice,90
#    2,Bob,85
#
#    JSON:
#    [{"id": "1", "name": "Alice", "score": "90"}, ...]

# 3. 自定义上下文管理器
#    实现一个 `SuppressErrors` 上下文管理器，它可以忽略代码块中抛出的特定异常。
#    with SuppressErrors(ZeroDivisionError):
#        print(1 / 0) # 不会报错，程序继续运行
#    print("Done")
```

---

## 📝 总结

- 永远使用 **`with` 语句** 来管理资源（文件、网络、锁）。
- 使用 **`pathlib`** 替代 `os.path`，代码更易读。
- `json` 和 `csv` 模块是数据交换的标准工具。

下一章：时间与日期的掌控！
