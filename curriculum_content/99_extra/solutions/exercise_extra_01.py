# exercise_extra_01.py - Reference Solution
# 参考答案

import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np
import random

# 1. 股票走势图 (Matplotlib)
def plot_stock_matplotlib():
    # 模拟数据
    days = list(range(1, 31))
    prices = [100]
    for _ in range(29):
        change = random.uniform(-5, 5)
        prices.append(prices[-1] + change)
        
    # 找出最高和最低点
    max_price = max(prices)
    max_day = days[prices.index(max_price)]
    min_price = min(prices)
    min_day = days[prices.index(min_price)]
    
    # 绘图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(days, prices, label="Stock Price", color="blue")
    
    # 标记最高点
    ax.annotate(f'Max: {max_price:.2f}', xy=(max_day, max_price), 
                xytext=(max_day+2, max_price+2),
                arrowprops=dict(facecolor='green', shrink=0.05))
                
    # 标记最低点
    ax.annotate(f'Min: {min_price:.2f}', xy=(min_day, min_price), 
                xytext=(min_day+2, min_price-2),
                arrowprops=dict(facecolor='red', shrink=0.05))
    
    ax.set_title("Simulated Stock Price (30 Days)")
    ax.set_xlabel("Day")
    ax.set_ylabel("Price ($)")
    ax.grid(True)
    ax.legend()
    
    print("Showing Matplotlib plot...")
    plt.show()


# 2. 散点图矩阵 (Plotly)
def plot_iris_plotly():
    # 获取内置数据集
    df = px.data.iris()
    
    # 绘图
    fig = px.scatter(df, 
                     x="sepal_width", 
                     y="sepal_length", 
                     color="species",
                     size="petal_length", # 气泡大小
                     hover_data=['petal_width'],
                     title="Iris Dataset: Sepal Dimensions")
                     
    print("Showing Plotly plot...")
    fig.show()


if __name__ == "__main__":
    # 运行 Matplotlib 示例
    plot_stock_matplotlib()
    
    # 运行 Plotly 示例
    plot_iris_plotly()
