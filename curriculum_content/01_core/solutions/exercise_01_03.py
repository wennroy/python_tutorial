# exercise_01_03.py - Reference Solution
# 参考答案

import datetime
import copy
import time

# 1. 修复陷阱：可变默认参数
def log_time(msg, logs=None):
    """
    修复后的函数，使用 None 作为默认值
    """
    if logs is None:
        logs = []
        
    now = datetime.datetime.now()
    logs.append((msg, now))
    return logs


# 2. 深浅拷贝大乱斗
def copy_experiment():
    print("--- 深浅拷贝实验 ---")
    
    # 原始数据
    data = {"ids": [1, 2, 3], "info": {"name": "test"}}
    
    # 创建三个变量
    ref_assign = data               # 赋值 (引用)
    shallow_cp = copy.copy(data)    # 浅拷贝
    deep_cp = copy.deepcopy(data)   # 深拷贝
    
    print(f"原始数据: {data}")
    
    # 修改原数据的内部列表
    print("\n>>> 修改原数据的 'ids' 列表 (append 4)...")
    data["ids"].append(4)
    
    # 修改原数据的内部字典
    print(">>> 修改原数据的 'info' 字典 (name -> modified)...")
    data["info"]["name"] = "modified"
    
    # 观察结果
    print(f"\n原始数据 (data):      {data}")
    print(f"赋值 (ref_assign):    {ref_assign}  <-- 完全同步")
    print(f"浅拷贝 (shallow_cp):  {shallow_cp}  <-- 内部对象受影响！")
    print(f"深拷贝 (deep_cp):     {deep_cp}     <-- 完全独立")


# 测试代码
if __name__ == "__main__":
    # 测试 1
    print("测试 log_time 函数:")
    log1 = log_time("First message")
    print("Log 1:", log1)
    
    # 模拟一点延迟，确保时间戳不同（虽然这里不是重点）
    time.sleep(0.1)
    
    log2 = log_time("Second message")
    print("Log 2:", log2) # 应该只包含 Second message，不包含 First message
    
    # 测试 2
    copy_experiment()
