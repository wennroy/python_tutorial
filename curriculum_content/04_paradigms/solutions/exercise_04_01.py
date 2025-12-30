# 模块 4-1 练习参考答案: OOP 角色系统

class Character:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp # 记录最大血量以便治疗

    def introduce(self):
        print(f"我是 {self.name}, 当前 HP: {self.hp}/{self.max_hp}")

    def attack(self, target):
        print(f"{self.name} 发起了普通攻击！")

class Warrior(Character):
    def __init__(self, name: str, hp: int, strength: int):
        super().__init__(name, hp)
        self.strength = strength

    def attack(self, target):
        damage = self.strength * 2
        target.hp -= damage
        print(f"{self.name} 挥舞巨剑砍向 {target.name}, 造成 {damage} 点伤害！")
        print(f"{target.name} 剩余 HP: {target.hp}")

class Healer(Character):
    def __init__(self, name: str, hp: int, mana: int):
        super().__init__(name, hp)
        self.mana = mana

    def heal(self, target):
        if self.mana >= 10:
            heal_amount = 20
            target.hp = min(target.max_hp, target.hp + heal_amount)
            self.mana -= 10
            print(f"{self.name} 为 {target.name} 施放了治疗术，恢复 {heal_amount} 点 HP！")
            print(f"{target.name} 当前 HP: {target.hp}")
        else:
            print(f"{self.name} 法力不足！")

# 测试代码
if __name__ == "__main__":
    arthur = Warrior("亚瑟", 100, 15)
    merlin = Healer("梅林", 60, 50)
    goblin = Character("哥布林", 80)

    arthur.introduce()
    merlin.introduce()

    # 战斗开始
    arthur.attack(goblin)
    
    # 模拟亚瑟受伤
    arthur.hp = 50
    print(f"\n亚瑟受伤了！当前 HP: {arthur.hp}")

    # 治疗
    merlin.heal(arthur)
