# 模块 1: Python 核心强化 - 字典与集合的奥秘

## 🎯 学习目标

完成本章后，你将能够：
- 理解哈希表（Hash Table）的基本原理
- 掌握字典（Dict）的高级用法 (`get`, `setdefault`, `defaultdict`)
- 熟练使用集合（Set）进行数学运算
- 理解为什么字典的查找速度如此之快

---

## 🪝 引言：如何快速找到联系人？

想象一下，你的通讯录里有 1000 个人。
如果你把他们写在一个长长的列表里，要找"张三"，你可能需要从头看到尾（O(n)）。
但如果你有一个索引页，直接翻到 "Z" 开头的那一页，瞬间就能找到（O(1)）。

这就是**字典**（Dictionary）的魔力。

---

## 🧠 核心概念：哈希表 (Hash Table)

Python 的 `dict` 和 `set` 底层都是基于**哈希表**实现的。

### 什么是哈希？
哈希函数就像一个"指纹提取器"，它能把任意长度的数据（如字符串 "apple"）转换成一个固定长度的数字（哈希值）。

```python
print(hash("apple"))
print(hash("banana"))
# 注意：列表是不可哈希的，不能作为字典的 Key！
# print(hash([1, 2])) # 会报错
```

### 字典的工作原理
1. 计算 Key 的哈希值。
2. 根据哈希值确定存储位置（索引）。
3. 直接存取 Value。

这就是为什么字典的查找、插入、删除操作平均时间复杂度都是 **O(1)**！

---

## 📚 字典进阶实战

### 1. 优雅地处理不存在的 Key

```python
data = {"name": "Alice", "age": 30}

# ❌ 危险的做法
# print(data["email"]) # KeyError!

# ✅ 安全的做法：get()
email = data.get("email", "未提供") # 如果不存在，返回默认值

# ✅ 设置默认值：setdefault()
# 如果 "role" 不存在，设为 "user" 并返回；如果存在，直接返回原值
role = data.setdefault("role", "user")
```

### 2. 字典推导式

就像列表推导式一样，字典也可以推导：

```python
names = ["Alice", "Bob", "Charlie"]
# 生成 {name: length}
name_lens = {name: len(name) for name in names}
print(name_lens) # {'Alice': 5, 'Bob': 3, 'Charlie': 7}
```

### 3. 神器：defaultdict

统计词频时，`defaultdict` 能省去很多判断代码。

```python
from collections import defaultdict

text = "apple banana apple orange banana apple"
words = text.split()

# 自动初始化为 0
counter = defaultdict(int)
for word in words:
    counter[word] += 1

print(dict(counter))
```

---

## 🔮 集合：数学的力量

集合（Set）就像是没有 Value 的字典，它只存储唯一的 Key。

### 1. 去重
```python
nums = [1, 2, 2, 3, 3, 3]
unique_nums = list(set(nums)) # [1, 2, 3]
```

### 2. 集合运算
集合运算非常适合处理"共同好友"、"差异对比"等场景。

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a & b) # 交集 (Intersection): {3, 4}
print(a | b) # 并集 (Union): {1, 2, 3, 4, 5, 6}
print(a - b) # 差集 (Difference): {1, 2} - 在 a 中但不在 b 中
print(a ^ b) # 对称差集 (Symmetric Difference): {1, 2, 5, 6} - 不共有的
```

---

## 🤖 AI 助手时间

> **Prompt**: "解释 Python 字典中的哈希冲突 (Hash Collision) 是什么，以及 Python 是如何解决它的？"
> 
> **Action**: 唤起 Copilot Chat 提问。
> 
> **Reflection**: AI 是否提到了"开放寻址法" (Open Addressing) 或 "链地址法" (Chaining)？Python 使用的是哪种？

---

## ✅ 动手挑战

创建文件 `exercise_01_02.py`，完成以下任务：

```python
# 1. 词频统计加强版
#    给定一段长文本，统计每个单词出现的次数，并找出出现频率最高的前 3 个单词。
#    提示：可以使用 collections.Counter

# 2. 集合运算实战
#    有两个列表：
#    class_a = ["Alice", "Bob", "Charlie", "David"]
#    class_b = ["Charlie", "David", "Eve", "Frank"]
#    找出：
#    - 两个班级都有的学生
#    - 只在 A 班的学生
#    - 所有的学生（不重复）

# 3. 字典转换
#    将 [("name", "Alice"), ("age", 30), ("city", "New York")] 转换为字典
```

---

## 📝 总结

- **字典**和**集合**利用哈希表实现了 O(1) 的极速查找。
- 只有**不可变**（Immutable）的对象才能作为字典的 Key 或集合的元素。
- 熟练使用 `get`, `defaultdict` 和集合运算能让代码更简洁高效。

下一章：内存管理与引用的深坑！
