# exercise_extra_02.py - Reference Solution
# 参考答案
# 运行方式: streamlit run exercise_extra_02.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Streamlit Exercise", layout="wide")

st.title("Streamlit 实战挑战 🚀")

# --- 任务 1: 交互式正态分布图 ---
st.header("1. 交互式正态分布图")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("参数配置")
    mu = st.slider("均值 (Mean)", -10.0, 10.0, 0.0, 0.1)
    sigma = st.slider("标准差 (Std)", 0.1, 5.0, 1.0, 0.1)

with col2:
    # 生成数据
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
    
    # 绘图
    fig, ax = plt.subplots()
    ax.plot(x, y, color='skyblue', linewidth=2)
    ax.fill_between(x, y, alpha=0.3, color='skyblue')
    ax.set_title(f"Normal Distribution ($\mu={mu}, \sigma={sigma}$)")
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)


st.markdown("---")

# --- 任务 2: 简单的 CSV 浏览器 ---
st.header("2. CSV 数据浏览器")

uploaded_file = st.file_uploader("上传一个 CSV 文件", type=["csv"])

if uploaded_file is not None:
    try:
        # 读取 CSV
        df = pd.read_csv(uploaded_file)
        
        st.success("文件上传成功！")
        
        # 显示前 5 行
        st.subheader("数据预览 (Top 5)")
        st.dataframe(df.head())
        
        # 显示统计信息
        st.subheader("统计信息")
        st.write(df.describe())
        
        # 简单的绘图 (如果包含数值列)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            st.subheader("快速绘图")
            col_to_plot = st.selectbox("选择一列进行绘图", numeric_cols)
            st.line_chart(df[col_to_plot])
            
    except Exception as e:
        st.error(f"解析文件时出错: {e}")
else:
    st.info("请上传文件以开始分析。")
