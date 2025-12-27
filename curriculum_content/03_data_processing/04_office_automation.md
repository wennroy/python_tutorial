# 模块 3: 数据处理与类型系统 - 办公自动化 (Office Automation)

## 🎯 学习目标

完成本章后，你将能够：
- 使用 `python-docx` 自动生成 Word 报告
- 结合 Pandas 和 Word，实现"数据 -> 图表 -> 报告"的全自动流程
- 理解自动化的价值：把重复劳动交给机器

---

## 🪝 引言：周报生成器

每周五下午，你都要从 Excel 里复制数据，粘贴到 Word 里，调整格式，生成周报。
这不仅无聊，还容易出错。
为什么不写个脚本，一键搞定呢？

---

## 🧠 核心概念：操作 Word 文档

我们需要安装 `python-docx` 库：
`pip install python-docx`

### 1. 创建文档

```python
from docx import Document
from docx.shared import Inches

# 创建新文档
doc = Document()

# 添加标题
doc.add_heading('Weekly Sales Report', 0)

# 添加段落
p = doc.add_paragraph('Here is the summary of this week.')
p.add_run(' bold text').bold = True
p.add_run(' and some ')
p.add_run('italic.').italic = True
```

### 2. 添加表格

```python
# 添加一个 2x2 的表格
table = doc.add_table(rows=2, cols=2)

# 填充表头
cell = table.cell(0, 0)
cell.text = "Product"
cell = table.cell(0, 1)
cell.text = "Sales"

# 填充数据
table.cell(1, 0).text = "Apple"
table.cell(1, 1).text = "100"
```

### 3. 添加图片

```python
# 假设你已经用 matplotlib 生成了一张图表 'chart.png'
doc.add_picture('chart.png', width=Inches(5))
```

### 4. 保存
```python
doc.save('report.docx')
```

---

## 🚀 实战：Pandas + Word 自动化流

这是最常见的企业级应用场景：
1. **Pandas**: 读取 Excel 数据，进行清洗、计算、统计。
2. **Matplotlib**: 将统计结果画成图表，保存为图片。
3. **python-docx**: 创建 Word，写入统计结论，插入图表。
4. **Email**: (可选) 自动发送邮件给老板。

---

## 🤖 AI 助手时间

> **Prompt**: "我想用 `python-docx` 修改一个现有的 Word 模板。模板里有一些占位符像 `{{name}}`。请帮我写一个函数，读取 docx 文件，替换所有的占位符，并保存为新文件。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 这是一个非常实用的需求（邮件合并 Mail Merge）。看看 AI 是如何遍历文档中的所有段落 (paragraphs) 和表格 (tables) 来查找替换文本的。

---

## ✅ 动手挑战

我们将使用 `exercise_03_04.py`。

**任务**：
1. 模拟生成一份销售数据 (Pandas DataFrame)。
2. 计算总销售额。
3. 生成一个 Word 文档：
    - 标题：Sales Report
    - 正文：Total sales is: $XXX
    - 表格：列出前 5 名的商品。

---

## 📝 总结

- **python-docx** 让 Word 变成了可编程对象。
- 结合 **Pandas**，你可以构建强大的自动化报告系统。
- 凡是需要"打开-复制-粘贴-保存"的重复工作，都应该被自动化。

恭喜！你已经完成了模块 3。你现在不仅能处理数据，还能让代码更健壮，甚至能自动写报告了！
