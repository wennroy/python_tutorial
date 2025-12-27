# 模块 1: Python 核心强化 - 内存管理与引用

## 🎯 学习目标

完成本章后，你将能够：
- 理解 Python 变量的本质（引用）
- 区分可变对象（Mutable）与不可变对象（Immutable）
- 掌握深拷贝（Deep Copy）与浅拷贝（Shallow Copy）的区别
- 避开"可变默认参数"这个经典大坑

---

## 🪝 引言：幽灵般的修改

先看一段代码，猜猜结果会是什么？

```python
a = [1, 2, 3]
b = a
b.append(4)

print(a) # 猜猜 a 是什么？
```

如果你认为 `a` 还是 `[1, 2, 3]`，那你可能把变量当成了"盒子"。
但在 Python 中，变量更像是**便利贴（标签）**。

---

## 🧠 核心概念：变量是标签，不是盒子

当你执行 `a = [1, 2, 3]` 时：
1. Python 在内存中创建了一个列表对象 `[1, 2, 3]`。
2. 把标签 `a` 贴在了这个对象上。

当你执行 `b = a` 时：
1. 你并没有复制那个列表。
2. 你只是把标签 `b` 也贴在了**同一个**对象上。

所以，通过 `b` 修改对象，`a` 也会看到变化，因为它们指向的是同一个东西！

我们可以用 `id()` 函数来验证：
```python
print(id(a))
print(id(b)) # 两个 ID 是一样的
print(a is b) # True
```

### 可变 vs 不可变

- **不可变 (Immutable)**: `int`, `float`, `str`, `tuple`
  - 一旦创建，内容不能改。修改意味着创建新对象。
- **可变 (Mutable)**: `list`, `dict`, `set`
  - 内容可以原地修改，ID 保持不变。

---

## 👯‍♀️ 深拷贝 vs 浅拷贝

如果我们真的想要一份独立的副本怎么办？

### 1. 浅拷贝 (Shallow Copy)
只复制最外层容器，里面的元素还是引用。

```python
import copy

list1 = [[1, 2], [3, 4]]
list2 = copy.copy(list1) # 或者 list1[:]

list2[0].append(99)
print(list1) # [[1, 2, 99], [3, 4]] - 内部列表还是受影响了！
```

### 2. 深拷贝 (Deep Copy)
递归地复制所有层级的对象，完全独立。

```python
list3 = copy.deepcopy(list1)
list3[0].append(888)
print(list1) # 不受影响
```

---

## ⚠️ 经典陷阱：可变默认参数

这是 Python 面试中最常见的问题之一：

```python
def add_item(item, box=[]):
    box.append(item)
    return box

print(add_item("apple")) # ['apple']
print(add_item("banana")) # ['apple', 'banana'] !!! 为什么 apple 还在？
```

**原因**：函数默认参数 `box=[]` 在函数**定义时**只创建一次。所有调用都共享同一个列表对象！

**修复方法**：使用 `None` 作为默认值。

```python
def add_item_safe(item, box=None):
    if box is None:
        box = []
    box.append(item)
    return box
```

---

## 🤖 AI 助手时间

> **Prompt**: "请画一个 ASCII 图来解释 Python 中 `a = [1, 2]; b = a` 和 `b = a[:]` 在内存结构上的区别。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: AI 画的图能帮你理解引用和拷贝的区别吗？

---

## ✅ 动手挑战

创建文件 `exercise_01_03.py`，完成以下任务：

```python
# 1. 修复陷阱
#    下面的函数试图在一个列表中追加时间戳，但它有 bug。请修复它。
#    import datetime
#    def log_time(msg, logs=[]):
#        now = datetime.datetime.now()
#        logs.append((msg, now))
#        return logs

# 2. 深浅拷贝大乱斗
#    创建一个包含列表的字典：data = {"ids": [1, 2, 3], "info": {"name": "test"}}
#    分别使用赋值(=)、浅拷贝(copy)、深拷贝(deepcopy)创建三个新变量。
#    修改原数据的内部列表和字典，观察三个新变量的变化，并打印结果验证你的理解。
```

---

## 📝 总结

- 变量存储的是对象的**引用**。
- `is` 比较引用（ID），`==` 比较值。
- 处理嵌套的可变对象时，小心使用**深拷贝**。
- 永远不要用可变对象作为函数的默认参数！

恭喜！你已经完成了 Python 核心强化模块。接下来，我们将进入调试艺术的世界！
