# exercise_03_01_advanced.py - Reference Solution
# 练习 03-01 (进阶): Pandas Groupby 与 迭代

import pandas as pd

def analyze_sales_advanced():
    # 1. 准备数据
    data = {
        "Category": ["Electronics", "Clothing", "Electronics", "Food", "Clothing", "Food", "Electronics"],
        "Product": ["Laptop", "T-Shirt", "Mouse", "Apple", "Jeans", "Bread", "Keyboard"],
        "Sales": [1000, 20, 50, 5, 40, 2, 80],
        "Profit": [200, 5, 10, 1, 8, 0.5, 20]
    }
    df = pd.DataFrame(data)
    print("原始数据:")
    print(df)
    print("-" * 30)

    # 2. 使用 Groupby 分析
    # 任务: 计算每个 Category 的总销售额和平均利润
    category_stats = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "mean"
    })
    print("\n按类别分组统计 (Groupby):")
    print(category_stats)
    
    # 3. 使用 iterrows 遍历 (演示目的)
    # 任务: 打印每一行，格式为 "Product: [Name], Margin: [Profit/Sales %]"
    print("\n使用 iterrows 遍历计算利润率:")
    for index, row in df.iterrows():
        # 注意: row 是一个 Series
        margin = (row["Profit"] / row["Sales"]) * 100
        print(f"Product: {row['Product']:<10} | Margin: {margin:.1f}%")

    # 4. 结构验证
    print("\n结构验证:")
    # 获取迭代器的第一个元素
    first_iter = next(df.iterrows())
    first_index = first_iter[0]
    first_row = first_iter[1]
    
    print(f"Row type: {type(first_row)}")
    print(f"Row index (original columns): {first_row.index.tolist()}")

if __name__ == "__main__":
    analyze_sales_advanced()
