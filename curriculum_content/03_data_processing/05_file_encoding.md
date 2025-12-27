# 模块 3: 数据处理与类型系统 - 文件编码与乱码生存指南

## 🎯 学习目标

完成本章后，你将能够：
- 理解 **字符编码** (Encoding) 的基本概念 (UTF-8, GBK, ASCII)
- 读懂并解决常见的 `UnicodeDecodeError` 错误
- 在 Python 和 Pandas 中正确处理不同编码的文件
- 掌握处理 "乱码" 的标准流程

---

## 🪝 引言：乱码的诅咒

你是否遇到过打开一个 CSV 文件，结果看到全是 `` 或者 `锟斤拷`？
这就是**编码问题**。在处理中文数据（尤其是来自 Windows 系统或老旧系统的文件）时，这是最令人头疼的拦路虎。如果不理解编码，你的数据处理脚本可能在第一步读取文件时就崩溃了。

---

## 🧠 核心概念：比特与字符

计算机只认识 0 和 1。
- **编码 (Encode)**: 将字符 (如 "中") 转换成 0/1 序列 (字节)。
- **解码 (Decode)**: 将 0/1 序列 (字节) 还原成字符。

如果编码和解码用的规则（密码本）不一样，就会出现乱码。

### 常见编码格式

1.  **UTF-8**: 万国码，互联网标准。**Linux/macOS 默认**。支持所有语言。
2.  **GBK / GB2312 / GB18030**: 中文编码。**中文 Windows 默认**。
3.  **ASCII**: 基础编码，只支持英文和数字。
4.  **Latin-1 (ISO-8859-1)**: 西欧语言，有时 Python 会默认回退到这个。

---

## 💥 常见错误与实战

### 1. 经典的 UnicodeDecodeError

这是最常见的报错。通常发生在你试图用 `UTF-8` 规则去解码一个 `GBK` 编码的文件时。

**场景模拟**:
假设我们有一个文件 `data_gbk.txt`，它是用 GBK 编码保存的，内容是 "你好"。

```python
# 错误示范：在 macOS/Linux 下默认使用 UTF-8 读取
try:
    with open("data_gbk.txt", "r") as f:
        content = f.read()
except UnicodeDecodeError as e:
    print(f"报错了: {e}")

# 可能的输出:
# 报错了: 'utf-8' codec can't decode byte 0xc4 in position 0: invalid continuation byte
```

**✅ 解决方案**: 显式指定 `encoding` 参数。

```python
# 正确示范
with open("data_gbk.txt", "r", encoding="gbk") as f:
    content = f.read()
print(content)

# 输出:
# 你好
```

### 2. Pandas 中的编码处理

Pandas 的 `read_csv` 默认也是 `utf-8`。如果读取 Excel 导出的 CSV (通常是 GBK)，需要指定编码。

```python
import pandas as pd

# 假设 sales.csv 是 GBK 编码
try:
    df = pd.read_csv("sales.csv")
except UnicodeDecodeError:
    print("读取失败，尝试使用 GBK...")
    df = pd.read_csv("sales.csv", encoding="gbk")

print(df.head())
```

### 3. 忽略错误 (慎用)

有时文件里混杂了非法字符，你可以选择忽略它们，但这会导致数据丢失。

```python
# errors='ignore': 丢弃无法解码的字符
# errors='replace': 用  替换无法解码的字符
with open("messy_data.txt", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()
```

---

## 🛠️ 实用技巧：如何猜测编码？

如果你不知道文件是什么编码，可以使用 `chardet` 库（需要安装）或者简单的试错法。

**常用试错顺序**:
1. `utf-8` (标准)
2. `gbk` (中文常见)
3. `latin-1` (如果不报错但乱码，通常是这个)

```python
def try_read_file(filepath):
    encodings = ['utf-8', 'gbk', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    return None, None
```

---

## 📝 练习

编写一个脚本，创建一个包含中文内容的 GBK 编码文件，然后尝试用不同的方式读取它，观察结果。
