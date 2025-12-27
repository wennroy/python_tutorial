# exercise_02_02.py - Data Processor
# 练习 02-02: 高级调试技巧 (条件断点 & 异常断点)

import time
import random

def process_data(data_id, value):
    """
    模拟数据处理函数
    """
    # 模拟耗时操作
    # time.sleep(0.01) 
    
    if data_id == "bad_id":
        # 这是一个隐藏的 Bug，只有特定 ID 会触发
        raise ValueError("Critical failure: Corrupted data block encountered!")
    
    return f"Processed {data_id}: {value * 2}"

def main():
    print("Starting batch processing...")
    
    # 生成 1000 条数据
    dataset = []
    for i in range(1000):
        dataset.append({"id": f"user_{i}", "value": i})
    
    # 插入一条脏数据
    random_index = random.randint(500, 900)
    dataset[random_index] = {"id": "bad_id", "value": 0}
    print(f"Inserted bad data at index {random_index} (but pretend you don't know this)")
    
    # 开始处理
    results = []
    for item in dataset:
        # 任务：
        # 1. 运行程序，它会崩溃。
        # 2. 使用 "Uncaught Exceptions" 断点捕获崩溃现场。
        # 3. 找出是哪个 ID 导致的。
        # 4. 设置条件断点 (item["id"] == "bad_id") 拦截它。
        # 5. 设置 Logpoint 打印 "Processing {item['id']}" 而不暂停。
        
        res = process_data(item["id"], item["value"])
        results.append(res)
        
    print("Batch processing complete.")

if __name__ == "__main__":
    main()
