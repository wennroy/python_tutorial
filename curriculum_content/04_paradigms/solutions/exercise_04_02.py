# 模块 4-1.5 练习参考答案: 进阶 OOP

from abc import ABC, abstractmethod
import threading

# 1. 抽象基类
class AbstractCharacter(ABC):
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def introduce(self):
        pass

# 2. 具体实现类
class Warrior(AbstractCharacter):
    def __init__(self, name, hp, strength):
        super().__init__(name, hp)
        self.strength = strength

    def attack(self, target):
        print(f"{self.name} (战士) 挥剑攻击 {target.name}，造成 {self.strength} 伤害")

    def introduce(self):
        print(f"我是战士 {self.name}, 力量: {self.strength}")

class Mage(AbstractCharacter):
    def __init__(self, name, hp, mana):
        super().__init__(name, hp)
        self.mana = mana

    def attack(self, target):
        print(f"{self.name} (法师) 发射火球攻击 {target.name}，消耗魔法")

    def introduce(self):
        print(f"我是法师 {self.name}, 魔法: {self.mana}")

# 3. 工厂模式
class CharacterFactory:
    @staticmethod
    def create(char_type, name):
        if char_type == "warrior":
            return Warrior(name, 100, 20)
        elif char_type == "mage":
            return Mage(name, 60, 100)
        else:
            raise ValueError(f"Unknown character type: {char_type}")

# 4. 单例模式 (线程安全)
class GameWorld:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(GameWorld, cls).__new__(cls)
                    cls._instance.characters = []
        return cls._instance

    def add_character(self, char):
        self.characters.append(char)
        print(f"{char.name} 加入了游戏世界。")

    def show_all(self):
        print(f"--- 当前世界有 {len(self.characters)} 名角色 ---")
        for char in self.characters:
            char.introduce()

# 测试代码
if __name__ == "__main__":
    # 测试单例
    world1 = GameWorld()
    world2 = GameWorld()
    print(f"World1 is World2: {world1 is world2}") # True

    # 使用工厂创建角色
    factory = CharacterFactory()
    c1 = factory.create("warrior", "亚瑟")
    c2 = factory.create("mage", "安吉拉")

    # 加入世界
    world1.add_character(c1)
    world2.add_character(c2) # world2 和 world1 是同一个实例

    world1.show_all()
