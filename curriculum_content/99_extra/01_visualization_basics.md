# 模块 Extra: 数据可视化基础 (Matplotlib & Plotly)

## 🎯 学习目标

完成本章后，你将能够：
- 使用 `matplotlib` 绘制基础图表（折线图、柱状图、散点图）
- 理解 Figure 和 Axes 的概念
- 使用 `plotly` 创建可交互的网页图表
- 让数据"讲故事"

---

## 🪝 引言：一图胜千言

给你一个包含 10,000 行销售数据的 Excel 表格，你能看出什么趋势吗？很难。
但如果画成一条折线图，你一眼就能看出哪个月销量暴跌了。

数据可视化是数据分析的最后一步，也是最重要的一步——展示结果。

---

## 📊 Matplotlib: 绘图界的鼻祖

Matplotlib 是 Python 最古老也最强大的绘图库。虽然默认样式有点"复古"，但它无所不能。

### 核心概念：画布 (Figure) 与 坐标系 (Axes)

想象你在画画：
- **Figure**: 整个画板。
- **Axes**: 画板上的一张纸（一个图表）。一个画板可以贴多张纸（子图）。

```python
import matplotlib.pyplot as plt

# 数据
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# 创建画板和坐标系
fig, ax = plt.subplots()

# 绘图
ax.plot(x, y, label="Linear", color="blue", linestyle="--")

# 装饰
ax.set_title("Simple Plot")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.legend()

# 显示
plt.show()
```

---

## 📈 Plotly: 现代交互式绘图

如果你想让图表动起来（鼠标悬停显示数值、缩放、拖拽），Plotly 是更好的选择。

```python
import plotly.express as px

# 准备数据 (通常是 DataFrame)
data = {
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
    "Number Eaten": [2, 1, 3, 1, 3, 2],
}

# 一行代码画图
fig = px.bar(data, x="Fruit", y="Number Eaten", color="Contestant", barmode="group")

# 显示 (会打开浏览器或在 Notebook 中显示)
fig.show()
```

---

## 🤖 AI 助手时间

> **Prompt**: "我有两个列表：dates (日期字符串) 和 values (数值)。请帮我用 matplotlib 画一个折线图，要求 X 轴日期标签旋转 45 度以免重叠，并添加网格线。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: AI 是如何处理日期格式化的？它用了 `plt.xticks(rotation=45)` 吗？

---

## ✅ 动手挑战

创建文件 `exercise_extra_01.py`，完成以下任务：

```python
# 1. 股票走势图 (Matplotlib)
#    模拟生成 30 天的股票价格数据（随机波动）。
#    绘制折线图，标记出最高价和最低价的点。

# 2. 散点图矩阵 (Plotly)
#    使用 Plotly Express 自带的 iris 数据集 (px.data.iris())。
#    绘制一个散点图，X 轴是 sepal_width，Y 轴是 sepal_length，颜色区分 species。
```

---

## 📝 总结

- **Matplotlib** 适合静态出版物、论文插图，控制力极强。
- **Plotly** 适合网页展示、数据探索，交互性好，API 简洁。
- 永远记得给图表加上 **Title**, **Label** 和 **Legend**，否则没人看得懂。

下一章：构建你的第一个数据看板 (Streamlit)！
