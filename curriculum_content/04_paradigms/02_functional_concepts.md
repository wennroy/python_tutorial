# 模块 4-2: 函数式编程思维 (Functional Programming Mindset)

## 1. 引言 (The Hook)
在 OOP 中，我们关注“对象”和“状态”的变化。而在**函数式编程 (FP)** 中，我们关注的是“数据流”和“变换”。

想象一条流水线：原材料（数据）进入，经过一系列机器（函数）的加工，最终变成成品。中间没有任何“全局变量”被修改，一切都是确定性的。

**本章学习目标**:
- 理解纯函数 (Pure Functions) 与副作用 (Side Effects)。
- 掌握高阶函数: `map`, `filter`, `reduce`。
- 学会使用 Lambda 表达式。

## 2. 核心概念 (The Concept)

### 纯函数 (Pure Functions)
*   **输入决定输出**: 只要输入参数相同，返回值永远相同。
*   **无副作用**: 不修改全局变量，不修改传入的可变对象，不打印日志（严格来说）。
*   *类比*: 数学函数 $f(x) = x + 1$。

### 高阶函数 (Higher-Order Functions)
函数可以作为参数传递给另一个函数，也可以作为返回值。这是 FP 的灵魂。

### Lambda 表达式
匿名函数，随用随扔。`lambda x: x * 2`。

## 3. 代码实战 (Code in Action)

**任务**: 将一个数字列表中的偶数挑出来，然后平方。

**方式 A: 命令式 (Imperative) - 怎么做**
```python
numbers = [1, 2, 3, 4, 5, 6]
result = []
for n in numbers:
    if n % 2 == 0:
        result.append(n ** 2)
print(result) # [4, 16, 36]
```

**方式 B: 函数式 (Functional) - 做什么**
```python
numbers = [1, 2, 3, 4, 5, 6]

# 1. Filter: 筛选偶数
evens = filter(lambda n: n % 2 == 0, numbers)

# 2. Map: 映射为平方
squared = map(lambda n: n ** 2, evens)

print(list(squared)) # [4, 16, 36]
```
*注意: Python 中更常用 **List Comprehension** (列表推导式) 来替代简单的 map/filter，但理解 map/filter 对学习 FP 至关重要。*

## 4. AI 结对编程 (Pair Programming with AI)

FP 的代码通常非常简洁，但有时难以阅读。AI 可以帮我们转换风格。

> 🤖 **AI 助手时间**:
> *   **场景**: 你有一段复杂的 `for` 循环代码。
> *   **Prompt**: 选中上面的“方式 A”代码，提问 "将这段代码重构为使用列表推导式 (List Comprehension) 的形式"。
> *   **Action**: 观察 Copilot 给出的单行解决方案。
> *   **Reflection**: 哪种方式更易读？如果逻辑非常复杂，一行代码写得下吗？

## 5. 动手挑战 (Hands-on Challenge)

**任务**: 数据清洗流水线。

1.  创建一个名为 `exercise_04_02.py` 的文件。
2.  定义一个包含用户数据的列表：
    ```python
    users = [
        {"name": "Alice", "age": 25, "email": "alice@example.com"},
        {"name": "Bob", "age": 16, "email": "bob@gmail.com"},
        {"name": "Charlie", "age": 30, "email": "charlie@example.com"},
        {"name": "David", "age": 17, "email": "david@hotmail.com"}
    ]
    ```
3.  使用 `filter` 和 `map` (或列表推导式) 完成以下步骤：
    *   筛选出成年人 (age >= 18)。
    *   提取他们的邮箱地址。
    *   将邮箱地址转换为小写。
4.  尝试用一行代码完成所有操作。

## 6. 总结与延伸 (Summary & Next Steps)
函数式编程让代码更易于测试和并行化，因为它避免了状态共享。

下一章，我们将对比 OOP 和 FP，并学习如何在实际项目中混合使用这两种范式。
