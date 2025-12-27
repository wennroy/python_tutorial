# 模块 3: 数据处理与类型系统 - Pandas 数据处理入门

## 🎯 学习目标

完成本章后，你将能够：
- 理解 **DataFrame** 和 **Series** 的核心概念
- 使用 Pandas 读取和保存 CSV/Excel 文件
- 掌握数据的**筛选**、**排序**和**基础统计**
- 告别 Excel 手动操作，实现数据处理自动化

---

## 🪝 引言：Excel 的极限

Excel 是世界上最流行的编程语言（没错，它是）。但当你有 100 万行数据，或者需要每天重复同样的清洗步骤时，Excel 就会卡死，而你的心态也会崩。
**Pandas** 是 Python 数据分析的瑞士军刀，它能让你像操作 SQL 一样高效地处理表格数据。

---

## 🧠 核心概念：表格的编程视角

### 1. DataFrame 与 Series

- **DataFrame**: 整个表格（类似于 Excel 的 Sheet）。
- **Series**: 表格中的一列（类似于 Excel 的 Column）。

```python
import pandas as pd

# 从字典创建 DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Paris", "London"]
}
df = pd.DataFrame(data)
print(df)
```

### 2. 读写文件 (IO)

Pandas 支持极其丰富的数据源。

```python
# 读取
df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# 写入
df.to_csv("output.csv", index=False) # index=False 不保存行号
df.to_excel("output.xlsx")
```

### 3. 数据筛选 (Selection)

```python
# 选择列
ages = df["Age"] # 返回 Series

# 选择行 (按条件)
adults = df[df["Age"] > 18]

# 复杂筛选 (AND &, OR |)
target = df[(df["Age"] > 25) & (df["City"] == "Paris")]
```

### 4. 基础统计

```python
print(df.describe()) # 快速查看 count, mean, std, min, max 等统计信息
print(df["Age"].mean()) # 计算平均年龄
print(df["City"].value_counts()) # 统计每个城市出现多少次
```

---

## 🌪️ 进阶操作：Groupby 与 迭代

### 1. 分组聚合 (Groupby)

这是 Pandas 最强大的功能之一，类似于 SQL 的 `GROUP BY` 或 Excel 的透视表。
核心思想是 **Split-Apply-Combine**（拆分-应用-合并）。

```python
# 假设我们有销售数据
df = pd.DataFrame({
    "Category": ["A", "B", "A", "B", "A"],
    "Sales": [100, 200, 150, 100, 300]
})

# 按 Category 分组，计算 Sales 的总和
grouped = df.groupby("Category")["Sales"].sum()
print(grouped)
# Category
# A    550
# B    300
# Name: Sales, dtype: int64

# 同时计算多个统计量
stats = df.groupby("Category").agg({
    "Sales": ["sum", "mean", "max"]
})
```

### 2. 遍历行 (Iteration)

虽然 Pandas 鼓励向量化操作（整列操作），但有时你不得不逐行处理。

**`iterrows()`**: 返回 (index, Series) 对。
- **Series** 是该行的数据，索引是列名。
- **注意**: `iterrows` 比较慢，处理大数据集时慎用。

```python
for index, row in df.iterrows():
    # row 是一个 Series 对象
    # 访问列：row["Category"] 或 row.Category
    print(f"Row {index}: {row['Category']} sold {row['Sales']}")
```

**`itertuples()`**: 返回命名元组 (namedtuple)。
- 比 `iterrows` 快很多。
- 访问列：`row.Category` (不能用 `row["Category"]`)。

```python
for row in df.itertuples():
    print(f"Row {row.Index}: {row.Category} sold {row.Sales}")
```

### 3. 结构辨析：Row vs DataFrame

初学者容易混淆：
- **DataFrame**: 二维表。`df.shape` 是 `(行数, 列数)`。
- **Series**: 一维数组（带索引）。`df["Col"]` 是 Series。
- **Row (from iterrows)**: 也是一个 **Series**！
    - 它的**索引 (Index)** 变成了原 DataFrame 的**列名**。
    - 它的**值 (Values)** 是该行的数据。

```python
# 取第一行
first_row = df.iloc[0] 
print(type(first_row)) # <class 'pandas.core.series.Series'>
print(first_row.index) # Index(['Category', 'Sales'], dtype='object')
```

---

## 🤖 AI 助手时间

> **Prompt**: "我有两个 DataFrame：`users` (id, name) 和 `orders` (order_id, user_id, amount)。请帮我写 Pandas 代码，将它们进行左连接 (Left Join)，并计算每个用户的总消费金额。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 看看 AI 是否使用了 `merge` 函数和 `groupby`？这是数据分析中最常用的两个操作。

---

## ✅ 动手挑战

我们将使用 `exercise_03_01.py`。你需要处理一份模拟的销售数据。

**任务**：
1. 创建一个包含 10 行数据的 DataFrame（包含 `Product`, `Price`, `Quantity`）。
2. 新增一列 `Total`，计算 `Price * Quantity`。
3. 筛选出 `Total` 大于 100 的订单。
4. 将结果保存为 `high_value_orders.csv`。

---

## 📝 总结

- **Pandas** 是 Python 数据处理的事实标准。
- 记住 **DataFrame** (表) 和 **Series** (列)。
- 善用 `read_csv` 和 `to_csv` 进行数据交换。
- 遇到复杂的数据清洗逻辑（如透视表、分组聚合），直接问 AI，它写 Pandas 比你快。

下一章：让 Python 代码更健壮——类型系统！
