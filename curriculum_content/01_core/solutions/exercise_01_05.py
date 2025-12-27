# exercise_01_05.py - Reference Solution
# 参考答案

from pathlib import Path
import csv
import json
import time

# 1. 目录扫描器
def scan_directory(path_str="."):
    p = Path(path_str)
    print(f"{'Filename':<30} | {'Lines':<10}")
    print("-" * 45)
    
    # 扫描所有 .py 文件
    for file_path in p.glob("**/*.py"): # ** 支持递归搜索
        try:
            # 读取行数
            content = file_path.read_text(encoding="utf-8")
            line_count = len(content.splitlines())
            print(f"{file_path.name:<30} | {line_count:<10}")
        except Exception as e:
            print(f"{file_path.name:<30} | Error: {e}")


# 2. JSON 转换器
def csv_to_json(csv_file, json_file):
    # 先创建一个测试用的 CSV
    if not Path(csv_file).exists():
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "score"])
            writer.writerow(["1", "Alice", "90"])
            writer.writerow(["2", "Bob", "85"])
    
    # 读取 CSV
    data = []
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
            
    # 写入 JSON
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Converted {csv_file} to {json_file}")


# 3. 自定义上下文管理器
class SuppressErrors:
    def __init__(self, error_type):
        self.error_type = error_type
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 如果发生了异常，且异常类型是我们想要忽略的
        if exc_type is not None and issubclass(exc_type, self.error_type):
            print(f"Suppressed error: {exc_val}")
            return True # 返回 True 表示异常被处理了，不再向上抛出
        return False # 返回 False 表示异常继续抛出


# 测试代码
if __name__ == "__main__":
    # 测试 1
    print("--- Directory Scan ---")
    scan_directory(".") # 扫描当前目录
    
    # 测试 2
    print("\n--- CSV to JSON ---")
    csv_to_json("test_data.csv", "test_data.json")
    
    # 测试 3
    print("\n--- Context Manager ---")
    print("Start")
    with SuppressErrors(ZeroDivisionError):
        print(1 / 0)
    print("End (Should be reached)")
