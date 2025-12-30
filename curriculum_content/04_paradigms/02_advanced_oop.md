# 模块 4-2: 进阶 OOP 与设计模式 (Advanced OOP & Design Patterns)

## 1. 引言 (The Hook)
在上一章，我们学会了如何创建角色。但随着游戏越来越复杂，你可能会遇到新的问题：
*   如何强制要求所有角色必须有 `attack` 方法？（防止队友写出没有攻击能力的 `Warrior`）
*   如何确保游戏中只有一个“游戏配置管理器”？（防止配置冲突）
*   如何根据玩家输入（"warrior", "mage"）动态创建角色，而不需要写一堆 `if-else`？

这就需要引入 **抽象 (Abstraction)** 和 **设计模式 (Design Patterns)**。

**本章学习目标**:
- 理解抽象基类 (Abstract Base Classes) 的作用。
- 掌握单例模式 (Singleton) 和工厂模式 (Factory)。
- 学会用 AI 辅助实现这些模式。

## 2. 抽象类 (Abstraction)

### 什么是抽象类？
抽象类是一个**不能被实例化**的类，它只定义了“接口”（Interface），即子类**必须**实现的方法。

### 为什么要用它？
它像是一份**契约**。如果你继承了 `AbstractCharacter`，你就必须实现 `attack` 方法，否则程序会报错。这在多人协作中非常重要。

```python
from abc import ABC, abstractmethod

class AbstractCharacter(ABC):
    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def move(self, x, y):
        pass

# class Ghost(AbstractCharacter):
#     pass
# ghost = Ghost() # 报错！因为没有实现 attack 和 move
```

## 3. 设计模式 (Design Patterns)

设计模式是前辈们总结出来的“常见问题的标准解决方案”。

### 3.1 单例模式 (Singleton)
**场景**: 游戏配置、数据库连接池、日志记录器。
**核心**: 确保一个类只有一个实例，并提供一个全局访问点。

```python
class GameConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("创建新的配置实例...")
            cls._instance = super(GameConfig, cls).__new__(cls)
            cls._instance.settings = {}
        return cls._instance

conf1 = GameConfig()
conf2 = GameConfig()

print(conf1 is conf2) # True
```

### 3.2 工厂模式 (Factory Pattern)
**场景**: 根据用户输入动态创建对象。
**核心**: 将对象的创建逻辑封装在一个工厂类中，客户端不需要知道具体的类名。

```python
class CharacterFactory:
    @staticmethod
    def create_character(char_type, name):
        if char_type == "warrior":
            return Warrior(name, 100, 15)
        elif char_type == "mage":
            return Mage(name, 60, 50)
        else:
            raise ValueError("未知的角色类型")

# 客户端代码
hero = CharacterFactory.create_character("warrior", "亚瑟")
```

## 4. AI 结对编程 (Pair Programming with AI)

设计模式的代码结构通常很固定，AI 非常擅长生成它们。

> 🤖 **AI 助手时间**:
> *   **场景**: 我们需要一个单例的 `DatabaseConnection` 类。
> *   **Prompt**: "使用 Python 的 `__new__` 方法实现一个线程安全的 Singleton 类 `DatabaseConnection`，模拟数据库连接。"
> *   **Action**: 观察 AI 是否使用了 `threading.Lock` 来保证线程安全？
> *   **Reflection**: 为什么单例模式在多线程环境下需要加锁？

## 5. 动手挑战 (Hands-on Challenge)

**任务**: 重构 RPG 系统。

1.  创建一个名为 `exercise_04_02.py` 的文件。
2.  定义 `AbstractCharacter` 抽象基类，强制要求实现 `attack` 和 `introduce`。
3.  实现 `Warrior` 和 `Mage` 继承该抽象类。
4.  实现 `CharacterFactory`，支持创建 `warrior` 和 `mage`。
5.  实现一个单例 `GameWorld` 类，用于管理所有的角色列表。
    *   拥有 `add_character(char)` 方法。
    *   拥有 `show_all_characters()` 方法。

## 6. 总结 (Summary)
抽象类提供了规范，设计模式提供了套路。掌握它们，你的代码将从“能跑就行”进化到“架构优雅”。

下一章，我们将回到函数式编程的世界。
