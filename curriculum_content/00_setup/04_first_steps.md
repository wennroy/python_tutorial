# 模块 0-4: 第一行代码与 AI 初体验

## 🎯 学习目标

完成本节后，你将能够：
- 编写并运行你的第一个 Python 脚本。
- 体验 GitHub Copilot 的代码补全功能。
- 完成本模块的实战练习。

---

## ⌨️ Hello, AI World!

让我们不再只打印 "Hello World"，而是让 AI 帮我们写点更有趣的。

1.  在你的工作区创建一个新文件 `hello_ai.py`。
2.  输入以下注释，然后**暂停**，等待 Copilot 的灰色建议出现：

```python
# 编写一个函数，随机生成一句问候语，包含时间（早上/下午/晚上）
```

3.  当灰色代码出现时，按 `Tab` 键接受。
4.  调用这个函数并打印结果。

### 运行代码
在终端中运行：
```bash
python hello_ai.py
```

---

## 🏋️‍♂️ 实战练习: 环境大体检

为了确保你的环境（Python + 虚拟环境 + IDE）真的万无一失，我们需要完成一个"体检"脚本。

### 任务描述
1.  在 `workspace` 目录下找到或创建 `exercise_00_01.py`。
2.  编写代码，打印出以下信息：
    *   当前 Python 版本 (`sys.version`)
    *   当前操作系统名称 (`os.name` 或 `platform.system()`)
    *   当前工作目录 (`os.getcwd()`)
    *   计算 $2^{10}$ 的值 (验证基本的数学运算)

### 💡 提示
你可以先写注释，让 Copilot 帮你生成代码。例如：
```python
# 导入 sys, os, platform 模块
# 打印当前 Python 版本
```

---

## 📝 提交与验证

当你完成代码并成功运行后，你应该能看到类似这样的输出：

```text
Python Version: 3.10.x ...
System: Darwin (macOS) / Windows
Current Directory: /Users/.../workspace
2 to the power of 10 is: 1024
```

如果你能看到这些，说明你的 **Module 0** 顺利通关！🎉

> 🤖 **AI 助手时间**:
> *   **Prompt**: "解释一下 `import sys` 和 `import os` 分别是做什么的？"
> *   **Action**: 选中代码，使用 Copilot Chat 提问。
