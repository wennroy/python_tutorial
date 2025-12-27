# exercise_05_01.py - Reference Solution
# 练习 05-01: 文件编码处理实战

import os
import pandas as pd

def encoding_practice():
    filename = "test_encoding_gbk.csv"
    
    # 1. 制造一个 GBK 编码的文件 (模拟 Windows Excel 导出的 CSV)
    # 内容: Name,City\n张三,北京\n李四,上海
    content = "Name,City\n张三,北京\n李四,上海"
    
    print(f"正在创建 GBK 编码文件: {filename} ...")
    with open(filename, "w", encoding="gbk") as f:
        f.write(content)
        
    print("-" * 30)

    # 2. 尝试用默认编码 (UTF-8) 读取
    print("尝试 1: 使用 UTF-8 读取 (预期会失败)")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            print(f.read())
    except UnicodeDecodeError as e:
        print(f"❌ 读取失败: {e}")
        print("原因: 文件是 GBK 编码，但我们试图用 UTF-8 解码。")

    print("-" * 30)

    # 3. 使用正确的编码读取
    print("尝试 2: 使用 GBK 读取 (预期成功)")
    try:
        with open(filename, "r", encoding="gbk") as f:
            data = f.read()
            print("✅ 读取成功:")
            print(data)
    except Exception as e:
        print(f"❌ 读取失败: {e}")

    print("-" * 30)

    # 4. Pandas 实战
    print("尝试 3: 使用 Pandas 读取")
    try:
        # 默认 read_csv 使用 utf-8
        df = pd.read_csv(filename)
    except UnicodeDecodeError:
        print("Pandas 默认读取失败，切换编码为 GBK...")
        df = pd.read_csv(filename, encoding="gbk")
    
    print("Pandas DataFrame 内容:")
    print(df)
    
    # 清理文件
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\n(已清理测试文件 {filename})")

if __name__ == "__main__":
    encoding_practice()
