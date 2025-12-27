# 模块 1: Python 核心强化 - 字符串处理与文本挖掘

## 🎯 学习目标

完成本章后，你将能够：
- 熟练掌握字符串的常用方法 (`split`, `join`, `strip`, `replace`)
- 深入理解 f-string 的高级格式化技巧
- 初步掌握正则表达式 (Regex) 的使用
- 学会处理编码问题 (Encoding)

---

## 🪝 引言：乱码与日志的噩梦

作为程序员，你一定遇到过这种情况：
从文件里读出来的中文变成了 `åäö` 这样的乱码；或者你需要从一堆杂乱无章的服务器日志中提取出所有的 IP 地址。

字符串处理是编程中最基础也最频繁的任务。掌握它，你就能从混乱的数据中提取价值。

---

## 🧠 核心概念：字符串不仅仅是文本

在 Python 中，字符串 (`str`) 是**不可变**的字符序列。

### 1. 常用方法组合拳

```python
raw_data = "  User: Alice, Age: 30,  City: New York  "

# 链式调用：去除首尾空格 -> 按逗号分割
parts = raw_data.strip().split(',') 
# ['User: Alice', ' Age: 30', '  City: New York']

# 列表推导式 + 再次处理
clean_data = [p.strip().split(': ')[1] for p in parts]
print(clean_data) # ['Alice', '30', 'New York']

# 拼接回去
print("|".join(clean_data)) # "Alice|30|New York"
```

### 2. f-string 的魔法

Python 3.6+ 引入的 f-string 不仅仅是变量替换。

```python
name = "Bob"
score = 0.87654
price = 123456789

print(f"User: {name.upper()}")          # 调用方法: USER: BOB
print(f"Score: {score:.2%}")            # 百分比格式化: Score: 87.65%
print(f"Price: ${price:,}")             # 千位分隔符: Price: $123,456,789
print(f"{name = }")                     # 调试神器 (3.8+): name = 'Bob'
```

### 3. 正则表达式 (Regular Expression)

当字符串方法不够用时（比如"提取所有邮箱"），正则就派上用场了。Python 使用 `re` 模块。

- `\d`: 数字
- `\w`: 字母或数字
- `+`: 一个或多个
- `*`: 零个或多个
- `?`: 零个或一个

```python
import re

text = "Contact us at support@example.com or sales@example.org."
# 简单的邮箱匹配模式
pattern = r"[\w\.-]+@[\w\.-]+\.\w+"

emails = re.findall(pattern, text)
print(emails) # ['support@example.com', 'sales@example.org']
```

---

## 🤖 AI 助手时间

> **Prompt**: "帮我写一个 Python 正则表达式，用于验证强密码：必须包含大小写字母、数字和特殊符号，长度至少 8 位。并解释每一部分的含义。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 正则表达式很难记？没关系，让 AI 帮你写，但你得能看懂它生成的解释。

---

## ✅ 动手挑战

创建文件 `exercise_01_04.py`，完成以下任务：

```python
# 1. 敏感词过滤
#    实现一个函数 censor_text(text, sensitive_words)，将 text 中的敏感词替换为 "*"
#    例如: censor_text("I hate you", ["hate"]) => "I **** you"
#    进阶：忽略大小写

# 2. 日志解析器
#    给定一段日志文本：
#    log = """
#    2023-10-01 10:00:01 [INFO] User logged in: user_123
#    2023-10-01 10:05:23 [ERROR] Database connection failed
#    2023-10-01 10:10:00 [INFO] User logged out: user_123
#    """
#    提取出所有的日志级别（INFO, ERROR）和时间戳。

# 3. 格式化输出
#    打印一个乘法表，要求对齐美观。
#    1 x 1 = 1
#    1 x 2 = 2   2 x 2 = 4
#    ...
#    提示：使用 f-string 的宽度控制，如 {x:2d}
```

---

## 📝 总结

- 字符串处理是数据清洗的第一步。
- 熟练使用 `strip`, `split`, `join` 能解决 80% 的问题。
- 遇到复杂模式匹配，大胆使用 **Regex**，但记得找 AI 帮忙写。
- **f-string** 是最现代、最强大的格式化方式。

下一章：文件 IO 与上下文管理器！
