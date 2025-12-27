# 模块 Extra: 动态可视化平台 (Streamlit)

## 🎯 学习目标

完成本章后，你将能够：
- 理解 Streamlit 的"脚本即应用"理念
- 使用 Streamlit 组件 (`st.write`, `st.slider`, `st.selectbox`)
- 结合 Pandas 和 Plotly 构建交互式数据看板
- 部署你的第一个 Web App

---

## 🪝 引言：从脚本到 App，只需几分钟

以前，如果你想把你的 Python 数据分析脚本变成一个网页分享给同事，你需要：
1. 学 HTML/CSS/JS 写前端。
2. 学 Flask/Django 写后端 API。
3. 处理前后端交互。

现在，有了 **Streamlit**，你只需要会写 Python。它能神奇地把你的脚本直接渲染成漂亮的 Web App。

---

## 🧠 核心概念：Script as App

Streamlit 的运行逻辑非常简单：**每当用户与界面交互（比如拖动滑块），整个脚本就会从头到尾重新运行一遍。**

### 1. 基础组件

```python
import streamlit as st
import pandas as pd
import numpy as np

st.title("我的第一个数据 App 🎈")

st.write("这里可以写 Markdown，也可以直接丢进去 DataFrame。")

# 输入组件
name = st.text_input("请输入你的名字", "Alice")
age = st.slider("选择你的年龄", 0, 100, 25)

st.write(f"你好, {name}! 你今年 {age} 岁了。")
```

### 2. 展示图表

Streamlit 原生支持 Matplotlib, Plotly, Altair 等多种绘图库。

```python
# 生成随机数据
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(chart_data) # 使用内置的简单图表
```

### 3. 布局 (Layout)

```python
col1, col2 = st.columns(2)

with col1:
    st.header("左边")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("右边")
    st.image("https://static.streamlit.io/examples/dog.jpg")
```

---

## 🚀 实战：股票数据看板

让我们把上一章学的 Plotly 结合进来。

```python
import streamlit as st
import plotly.express as px

# 侧边栏配置
st.sidebar.header("配置项")
symbol = st.sidebar.selectbox("选择股票", ["AAPL", "GOOGL", "TSLA"])

# 模拟数据获取
st.write(f"正在分析 {symbol} 的数据...")
# ... (此处省略数据获取代码)

# 绘图
# fig = px.line(...)
# st.plotly_chart(fig)
```

---

## 🤖 AI 助手时间

> **Prompt**: "我有一个 CSV 文件 `sales.csv`，包含 `date`, `region`, `amount` 三列。请帮我写一个完整的 Streamlit App 代码，包含一个侧边栏用于筛选 `region`，主界面显示该地区的销售额折线图。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 看看 AI 是否使用了 `st.sidebar`？它是如何根据筛选条件过滤 DataFrame 的？

---

## ✅ 动手挑战

创建文件 `exercise_extra_02.py`，完成以下任务：

**注意**：运行 Streamlit 应用需要使用命令 `streamlit run exercise_extra_02.py`，而不是直接运行 Python 文件。

```python
# 1. 交互式正态分布图
#    创建一个 App，包含两个滑块：
#    - 均值 (Mean): 范围 -10 到 10
#    - 标准差 (Std): 范围 0.1 到 5
#    根据滑块的值，实时绘制正态分布曲线 (使用 Matplotlib 或 Plotly)。

# 2. 简单的 CSV 浏览器
#    使用 st.file_uploader 让用户上传一个 CSV 文件。
#    上传成功后，显示前 5 行数据，并显示数据的统计信息 (df.describe())。
```

---

## 📝 总结

- **Streamlit** 是数据科学家展示成果的神器。
- 它的核心逻辑是**重运行 (Rerun)**，所以要注意性能（使用 `@st.cache_data` 缓存数据）。
- 它可以轻松部署到 Streamlit Cloud 或私有服务器。

恭喜！你现在已经具备了全栈数据应用开发的能力了！
