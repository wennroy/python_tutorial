# 模块 4-3: 范式大对决与重构 (Paradigm Showdown & Refactoring)

## 1. 引言 (The Hook)
手里拿着锤子，看什么都像钉子。如果你只懂 OOP，你可能会创建 `AbstractIntegerFactory` 来做一个加法。如果你只懂 FP，你可能会为了打印一行日志而引入复杂的 Monad。

Python 是一门**多范式 (Multi-paradigm)** 语言。最好的 Python 程序员懂得在适当的时候选择适当的工具。

**本章学习目标**:
- 对比 OOP 与 FP 的优缺点。
- 学习如何在 Python 中混合使用两种范式。
- 实战：利用 AI 将 OOP 代码重构为 FP 风格。

## 2. 核心概念 (The Concept)

| 特性 | 面向对象 (OOP) | 函数式 (FP) |
| :--- | :--- | :--- |
| **核心单元** | 类 (Class) & 对象 | 函数 (Function) |
| **状态管理** | 封装在对象内部 (Stateful) | 避免状态，数据不可变 (Stateless) |
| **主要用途** | GUI, 游戏, 复杂业务模型 | 数据处理, 并发系统, 算法逻辑 |
| **优点** | 直观，易于模拟现实世界 | 易测试，无副作用，易并行 |
| **缺点** | 容易产生复杂的继承关系和状态同步问题 | 学习曲线陡峭，有时过于抽象 |

**最佳实践**:
*   **宏观架构用 OOP**: 比如设计一个 Web 服务器，`Request`, `Response`, `User` 很适合作为对象。
*   **微观逻辑用 FP**: 比如处理 `User` 对象中的数据列表，使用 `map`/`filter` 比 `for` 循环更清晰。

## 3. 代码实战 (Code in Action)

**场景**: 购物车计算总价。

**OOP 风格**:
```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, price):
        self.items.append(price)

    def calculate_total(self):
        return sum(self.items)

cart = ShoppingCart()
cart.add_item(10)
cart.add_item(20)
print(cart.calculate_total())
```

**FP 风格**:
```python
def add_item(cart, price):
    return cart + [price] # 返回新列表，不修改原列表

def calculate_total(cart):
    return sum(cart)

cart = []
cart = add_item(cart, 10)
cart = add_item(cart, 20)
print(calculate_total(cart))
```

## 4. AI 结对编程 (Pair Programming with AI)

重构是程序员的日常，而 AI 是重构的神器。

> 🤖 **AI 助手时间**:
> *   **场景**: 你接手了一段充满“坏味道”的 OOP 代码，里面全是全局变量和复杂的类继承。
> *   **Prompt**: "这段代码使用了过度的 OOP 设计。请将其重构为简单的函数式风格，移除不必要的类，使用纯函数处理数据。"
> *   **Action**: 观察 AI 如何拆解类的方法。
> *   **Reflection**: 重构后的代码行数减少了吗？逻辑是否更清晰了？

## 5. 动手挑战 (Hands-on Challenge)

**任务**: 重构 `TextProcessor`。

1.  创建一个名为 `exercise_04_03.py` 的文件。
2.  复制以下 OOP 代码：
    ```python
    class TextProcessor:
        def __init__(self, text):
            self.text = text

        def clean(self):
            self.text = self.text.strip().lower()

        def remove_special_chars(self):
            import re
            self.text = re.sub(r'[^a-z0-9\s]', '', self.text)

        def get_words(self):
            return self.text.split()

    processor = TextProcessor("  Hello, World! 123  ")
    processor.clean()
    processor.remove_special_chars()
    print(processor.get_words())
    ```
3.  **挑战**: 不使用任何类，只使用函数来实现相同的功能。
    *   提示：定义 `clean_text(text)`, `remove_special(text)` 等函数，每个函数接收字符串并返回处理后的字符串。
4.  使用 Copilot 帮你生成测试用例来验证两种实现的结果是否一致。

## 6. 总结 (Summary)
恭喜你完成了编程范式的学习！现在你已经掌握了 Python 的两把利剑。

在接下来的模块中，我们将学习如何组织更大的代码库——**包设计与模块化**。
