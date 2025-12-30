# 模块 4-5: 常用设计模式实战 (Common Design Patterns & Pipeline)

## 1. 引言 (The Hook)
设计模式不仅仅是面试题，它们是解决特定问题的“瑞士军刀”。在前面的章节中，我们学习了单例和工厂模式。今天，我们将补充几个在 Python 项目中极其实用的模式，特别是你点名想要的 **管道模式 (Pipeline Pattern)**。

**本章学习目标**:
- 掌握 **策略模式 (Strategy)**：优雅地替换算法。
- 掌握 **观察者模式 (Observer)**：实现事件通知机制。
- 掌握 **装饰器模式 (Decorator)**：Pythonic 的功能增强方式。
- 重点掌握 **管道模式 (Pipeline)**：构建清晰的数据处理流。

## 2. 策略模式 (Strategy Pattern)
**场景**: 你在做一个电商系统，支持支付宝、微信、信用卡支付。
**痛点**: 写了一堆 `if payment_type == 'alipay': ... elif ...`。
**解决方案**: 把每种支付方式封装成一个独立的类（或函数），让它们可以互换。

```python
from abc import ABC, abstractmethod

# 1. 定义策略接口
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): pass

# 2. 具体策略
class Alipay(PaymentStrategy):
    def pay(self, amount): print(f"支付宝支付: {amount} 元")

class CreditCard(PaymentStrategy):
    def pay(self, amount): print(f"信用卡支付: {amount} 元")

# 3. 上下文 (Context)
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy
    
    def execute_payment(self, amount):
        self.strategy.pay(amount)

# 使用
ctx = PaymentContext(Alipay())
ctx.execute_payment(100)
```

## 3. 观察者模式 (Observer Pattern)
**场景**: 当“股票价格”更新时，自动通知“散户”、“机构”和“APP推送”。
**解决方案**: “被观察者”维护一份“观察者”名单，数据变化时遍历名单调用通知方法。

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def update(self, message):
        print(f"收到通知: {message}")

# 使用
news_channel = Subject()
subscriber1 = Observer()
news_channel.attach(subscriber1)
news_channel.notify("比特币涨破 10 万美元！")
```

## 4. 管道模式 (Pipeline Pattern)
**场景**: 数据处理流水线。例如：爬虫数据 -> 清洗 -> 去重 -> 存库。
**核心**: 将复杂的处理逻辑拆分成一个个独立的“阶段” (Stage)，数据像水流一样流过管道。

### 4.1 面向对象实现
```python
class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage_func):
        self.stages.append(stage_func)
        return self # 支持链式调用

    def process(self, data):
        for stage in self.stages:
            data = stage(data)
        return data

# 定义处理阶段
def remove_whitespace(text): return text.strip()
def to_lower(text): return text.lower()
def remove_punctuation(text): 
    import re
    return re.sub(r'[^\w\s]', '', text)

# 组装管道
pipe = Pipeline()
pipe.add_stage(remove_whitespace).add_stage(to_lower).add_stage(remove_punctuation)

raw_data = "  Hello, World!!!  "
result = pipe.process(raw_data)
print(f"结果: '{result}'") # 结果: 'hello world'
```

### 4.2 函数式实现 (高级)
使用 `functools.reduce` 可以一行代码实现管道。
```python
from functools import reduce

def pipeline(data, *functions):
    return reduce(lambda val, func: func(val), functions, data)

result = pipeline("  HI  ", remove_whitespace, to_lower)
```

## 5. 装饰器模式 (Decorator Pattern)
Python 内置了对装饰器的支持，这本质上就是装饰器模式。
**场景**: 给函数增加日志、计时、权限校验功能，但不修改函数本身。

```python
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时: {end - start:.4f}s")
        return result
    return wrapper

@timer_decorator
def slow_task():
    time.sleep(0.5)

slow_task()
```

## 6. AI 结对编程 (Pair Programming with AI)

> 🤖 **AI 助手时间**:
> *   **场景**: 你想实现一个更复杂的管道，支持“异常处理”。如果中间某个步骤出错了，管道应该怎么做？
> *   **Prompt**: "请帮我修改 Python 的 Pipeline 类，增加错误处理机制。如果某个 stage 抛出异常，记录日志并停止处理，返回 None。"
> *   **Action**: 观察 AI 如何使用 `try-except` 包裹循环体。

## 7. 动手挑战 (Hands-on Challenge)

**任务**: 构建一个“订单处理系统”。

1.  创建一个名为 `exercise_04_05.py` 的文件。
2.  **需求**:
    *   使用 **Pipeline 模式** 处理订单数据：`验证库存` -> `计算折扣` -> `生成发票`。
    *   使用 **Strategy 模式** 处理支付：支持 `CreditCard` 和 `PayPal`。
    *   使用 **Decorator 模式** 记录订单处理的时间。
3.  模拟一个订单字典 `order = {"item": "Book", "price": 100, "qty": 2}`，让它流过你的系统。

## 8. 总结 (Summary)
设计模式是编程的“内功”。
*   **Strategy**: 消除 `if-else`。
*   **Observer**: 解耦通知。
*   **Pipeline**: 拆解复杂流程。
*   **Decorator**: 无痛增强功能。

掌握这些，你的代码质量将上一个台阶！
