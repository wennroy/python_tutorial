# 模块 4-1: 面向对象编程基础 (OOP Foundations)

## 1. 引言 (The Hook)
想象一下你在开发一个 RPG 游戏。你需要创建成百上千个角色：战士、法师、弓箭手... 如果用普通的变量和函数来写，你可能会陷入“变量地狱”：`warrior1_hp`, `warrior1_attack`, `mage1_mana`... 

**面向对象编程 (OOP)** 就是为了解决这个问题而生的。它允许我们将数据（属性）和行为（方法）打包成一个“蓝图”（类），然后根据这个蓝图批量制造“产品”（对象）。

**本章学习目标**:
- 理解类 (Class) 与对象 (Object) 的区别。
- 掌握继承 (Inheritance) 与多态 (Polymorphism) 的核心机制。
- 理解 Python 特有的“鸭子类型” (Duck Typing)。
- 学会使用 Copilot 快速生成样板代码。

## 2. 核心概念 (The Concept)

### 类 (Class) vs 对象 (Object)
*   **类 (Class)**: 就像是**模具**或**图纸**。它定义了角色应该有什么属性（名字、血量）和什么技能（攻击、移动）。
*   **对象 (Object)**: 就像是用模具造出来的**具体手办**。每一个手办都有自己独特的名字和状态。

### 继承 (Inheritance)
不想重复造轮子？如果 `Warrior` 和 `Mage` 都有名字和血量，我们可以创建一个通用的 `Character` 类，然后让它们**继承**它。

### 多态 (Polymorphism)
同一个接口，不同的表现。`Warrior.attack()` 可能是挥剑，`Mage.attack()` 可能是丢火球。调用者不需要知道具体是哪个职业，只需要调用 `.attack()` 即可。

## 2.1 深入理解继承与多态 (Deep Dive)

### `super()` 到底是什么？
你可能认为 `super()` 只是调用父类。但在多重继承中，它其实是按照 **MRO (Method Resolution Order)** 的顺序来查找下一个类。
*   **最佳实践**: 始终使用 `super().__init__()` 而不是 `Parent.__init__(self)`，以确保在复杂的继承关系中每个类只被初始化一次。

### 鸭子类型 (Duck Typing)
Python 是动态语言，它不强制要求继承。
> "如果它走起路来像鸭子，叫起来像鸭子，那它就是鸭子。"

只要一个对象实现了 `attack()` 方法，它就可以被当作“战士”来使用，哪怕它并没有继承 `Character` 类。这就是 Python 灵活性的来源。

## 3. 代码实战 (Code in Action)

让我们来定义一个基础的角色系统：

```python
class Character:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp

    def introduce(self):
        print(f"我是 {self.name}, 当前 HP: {self.hp}")

    def attack(self, target):
        print(f"{self.name} 发起了普通攻击！")

# 继承自 Character
class Warrior(Character):
    def __init__(self, name: str, hp: int, strength: int):
        super().__init__(name, hp) # 调用父类初始化
        self.strength = strength

    # 重写 (Override) 父类方法 -> 多态
    def attack(self, target):
        damage = self.strength * 2
        print(f"{self.name} 挥舞巨剑砍向 {target.name}, 造成 {damage} 点伤害！")

# 实例化对象
hero = Warrior("亚瑟", 100, 15)
monster = Character("哥布林", 50)

hero.introduce()
hero.attack(monster)
```

## 4. AI 结对编程 (Pair Programming with AI)

OOP 的代码往往比较冗长（Boilerplate code），这正是 AI 擅长的地方。

> 🤖 **AI 助手时间**:
> *   **场景**: 我们需要增加一个 `Mage` (法师) 类。
> *   **Prompt**: 在 `Warrior` 类下面，输入注释 `# 创建一个 Mage 类，继承自 Character，拥有 mana 属性，attack 方法消耗 mana 发射火球`。
> *   **Action**: 等待 Copilot 自动补全代码。
> *   **Reflection**: 检查 Copilot 是否正确调用了 `super().__init__`？它是否理解了“消耗 mana”的逻辑？

## 5. 动手挑战 (Hands-on Challenge)

**任务**: 完善这个 RPG 系统。

1.  创建一个名为 `exercise_04_01.py` 的文件。
2.  定义 `Character` 基类。
3.  使用 Copilot 辅助生成 `Healer` (治疗者) 类：
    *   拥有 `heal(target)` 方法，可以恢复目标角色的 HP。
4.  编写一段测试代码，让一个 `Warrior` 攻击，然后 `Healer` 为其治疗。

## 6. 总结与延伸 (Summary & Next Steps)
OOP 让我们能以更接近人类思维的方式组织代码。通过类和继承，我们实现了代码的复用和逻辑的封装。

下一章，我们将深入探讨 OOP 的高级话题：**抽象类与设计模式**，看看如何像架构师一样设计代码。
