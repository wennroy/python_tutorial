# exercise_03_01.py - Reference Solution
# 练习 03-01: Pandas 基础

import pandas as pd
import numpy as np

def process_sales_data():
    # 1. 创建 DataFrame
    data = {
        "Product": [f"Item_{i}" for i in range(1, 11)],
        "Price": np.random.randint(10, 100, 10), # 随机价格 10-100
        "Quantity": np.random.randint(1, 5, 10)  # 随机数量 1-5
    }
    df = pd.DataFrame(data)
    
    print("原始数据:")
    print(df)
    
    # 2. 新增 Total 列
    df["Total"] = df["Price"] * df["Quantity"]
    
    # 3. 筛选 Total > 100 的订单
    high_value_orders = df[df["Total"] > 100]
    
    print("\n高价值订单 (>100):")
    print(high_value_orders)
    
    # 4. 保存结果
    output_file = "high_value_orders.csv"
    high_value_orders.to_csv(output_file, index=False)
    print(f"\n结果已保存至 {output_file}")

if __name__ == "__main__":
    process_sales_data()
