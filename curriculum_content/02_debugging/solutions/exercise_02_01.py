# exercise_02_01.py - Buggy Calculator
# 练习 02-01: 调试器入门

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        # Bug 1: 字符串拼接而不是数值相加
        result = str(a) + str(b)
        self.history.append(f"Added {a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        # Bug 2: 忘记添加到历史记录
        return result

    def get_last_operation(self):
        # Bug 3: 如果历史记录为空，这里会报错
        return self.history[-1]

if __name__ == "__main__":
    calc = Calculator()
    
    print("Testing Addition:")
    res1 = calc.add(1, 1)
    print(f"1 + 1 = {res1}") # 期望 2，实际 11
    
    print("\nTesting Subtraction:")
    res2 = calc.subtract(10, 5)
    print(f"10 - 5 = {res2}")
    
    print("\nHistory:")
    print(calc.history) # 期望包含减法记录，实际没有
    
    # 尝试获取最后一次操作
    # 如果我们只做减法（没有记录历史），这里可能会崩
    # print(calc.get_last_operation())
