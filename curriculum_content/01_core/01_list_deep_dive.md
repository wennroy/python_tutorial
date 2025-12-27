# 模块 1: Python 核心强化 - List 深度解析

## 🎯 学习目标

完成本章后，你将能够：
- 理解 Python 列表的底层实现原理
- 熟练使用切片操作
- 掌握列表推导式的各种用法
- 了解常见操作的时间复杂度

---

## 🪝 引言：列表无处不在

打开你的手机，你的通讯录是一个列表；你的购物车是一个列表；你的微信聊天记录也是一个列表。

在 Python 中，`list` 是最常用的数据结构之一。但你真的了解它吗？

---

## 🧠 核心概念：列表的本质

### 列表是动态数组

Python 的列表底层是一个**动态数组**（Dynamic Array），它：
- 存储的是对象的**引用**（指针），而不是对象本身
- 当容量不足时，会自动扩容（通常是当前容量的 1.125 倍）

```python
# 看看列表占用的内存
import sys

lst = []
print(f"空列表: {sys.getsizeof(lst)} bytes")

for i in range(10):
    lst.append(i)
    print(f"长度 {len(lst)}: {sys.getsizeof(lst)} bytes")
```

---

## 🔪 切片操作：列表的瑞士军刀

切片语法：`list[start:stop:step]`

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 基础切片
print(nums[2:5])      # [2, 3, 4] - 从索引2到4
print(nums[:3])       # [0, 1, 2] - 前3个
print(nums[-3:])      # [7, 8, 9] - 后3个

# 带步长
print(nums[::2])      # [0, 2, 4, 6, 8] - 每隔一个
print(nums[::-1])     # [9, 8, 7, ...] - 反转列表！

# 实用技巧：复制列表
copy = nums[:]        # 浅拷贝
```

---

## 🚀 列表推导式：Pythonic 的艺术

列表推导式让你用一行代码完成复杂的列表生成：

```python
# 传统方式
squares = []
for x in range(10):
    squares.append(x ** 2)

# 列表推导式
squares = [x ** 2 for x in range(10)]

# 带条件
evens = [x for x in range(20) if x % 2 == 0]

# 嵌套
matrix = [[i * j for j in range(5)] for i in range(5)]
```

---

## ⏱️ 时间复杂度速查表

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `append()` | O(1)* | 均摊时间 |
| `pop()` | O(1) | 删除末尾 |
| `pop(0)` | O(n) | 删除开头，需要移动所有元素！ |
| `insert(i, x)` | O(n) | 中间插入 |
| `x in list` | O(n) | 线性查找 |
| `list[i]` | O(1) | 索引访问 |

> ⚠️ **陷阱警告**：频繁使用 `pop(0)` 或 `insert(0, x)`？考虑使用 `collections.deque`！

---

## 🤖 AI 助手时间

> **Prompt**: "解释为什么 Python 列表的 `pop(0)` 是 O(n) 而 `pop()` 是 O(1)"
> 
> **Action**: 选中上面的时间复杂度表格，使用 `Cmd+I` (macOS) 或 `Ctrl+I` (Windows) 唤起 Copilot Chat。
> 
> **Reflection**: AI 的解释是否提到了"数组元素移动"？

---

## ✅ 动手挑战

创建文件 `exercise_01_01.py`，完成以下任务：

```python
# 1. 使用列表推导式生成 1-100 中所有能被 3 或 5 整除的数

# 2. 实现一个函数，将嵌套列表展平
#    flatten([[1, 2], [3, 4], [5]]) => [1, 2, 3, 4, 5]

# 3. 使用切片实现字符串反转，并检查是否是回文
#    is_palindrome("racecar") => True
```

---

## 📝 总结

今天我们学习了：
- 列表的底层是**动态数组**
- **切片**是处理列表的强大工具
- **列表推导式**让代码更 Pythonic
- 注意操作的**时间复杂度**

下一章：字典 (Dict) 与集合 (Set) 的奥秘！
