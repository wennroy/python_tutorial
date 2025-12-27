# exercise_03_02.py - Reference Solution
# 练习 03-02: 类型系统基础 & 进阶

from typing import Optional, Union, List

# 任务 1: 基础注解
def greeting(name: str) -> str:
    return f"Hello, {name}"

# 任务 2: 进阶注解 (Optional, Union)
def safe_divide(a: Union[int, float], b: Union[int, float]) -> Optional[float]:
    """
    安全除法，如果分母为 0 返回 None
    """
    if b == 0:
        return None
    return float(a) / float(b)

# 任务 3: 容器类型
def process_scores(scores: List[int]) -> float:
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

# 测试代码
if __name__ == "__main__":
    # 正常调用
    print(greeting("Alice"))
    
    res1 = safe_divide(10, 2)
    print(f"10 / 2 = {res1}")
    
    res2 = safe_divide(5, 0)
    if res2 is None:
        print("5 / 0 = None (Safe!)")
        
    avg = process_scores([80, 90, 100])
    print(f"Average: {avg}")
    
    # 错误类型调用 (IDE 应该会警告，mypy 会报错)
    # greeting(123) 
    # safe_divide("10", "2")
