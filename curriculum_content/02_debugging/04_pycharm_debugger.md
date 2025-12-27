# 模块 2: 调试艺术 - PyCharm 调试器指南

## 🎯 学习目标

完成本章后，你将能够：
- 熟练使用 PyCharm 强大的可视化调试器
- 掌握 **Smart Step Into** 这一杀手级功能
- 使用 **Evaluate Expression** 动态求值
- 利用 **Inline Values** 快速查看变量状态

---

## 🪝 引言：JetBrains 的魔法

如果你是 PyCharm 的用户，恭喜你，你手中拥有的是 Python 届最强大的调试武器之一。
PyCharm 的调试器以"智能"著称，它能猜到你想看什么，甚至在你把鼠标放上去之前就把变量值显示在代码行旁边了。

---

## 🧠 核心概念：调试面板概览

### 1. 启动调试 (Debug)

点击右上角的绿色甲虫图标 🐞 (Debug)，或者按下快捷键：
- **Windows/Linux**: `Shift + F9`
- **macOS**: `Ctrl + D`

### 2. 断点 (Breakpoints) 🔴

和 VS Code 一样，点击行号右侧的空白处即可。
**高级技巧**: 右键点击断点，可以设置 **Condition** (条件) 或取消勾选 **Suspend** (不暂停，仅记录日志)。

### 3. 调试控制条 (Debug Tool Window)

当程序暂停时，底部面板会激活。

- **Variables**: 显示当前作用域变量。
- **Frames**: 调用堆栈。
- **Watches**: 可以在这里添加你想持续监控的表达式。

---

## 🎮 操控流程：快捷键指南

PyCharm 的快捷键逻辑与 VS Code 略有不同（默认 Keymap）：

| 功能 | Windows / Linux | macOS | 说明 |
|------|----------------|-------|------|
| **Step Over** (单步跳过) | `F8` | `F8` | 最常用的键，一行行执行 |
| **Step Into** (单步调试) | `F7` | `F7` | 进入函数内部 |
| **Smart Step Into** | `Shift + F7` | `Shift + F7` | **神器！** 下面详细介绍 |
| **Step Out** (单步跳出) | `Shift + F8` | `Shift + F8` | 跳出当前函数 |
| **Resume Program** (继续) | `F9` | `Cmd + Opt + R` | 运行到下一个断点 |

---

## 💎 PyCharm 独门绝技

### 1. 智能步进 (Smart Step Into)

假设你有一行代码：
```python
result = process(calculate(a), get_modifier(b))
```
如果你按普通的 `Step Into` (F7)，调试器通常会按顺序进入 `calculate`，然后你得跳出，再进入 `get_modifier`... 很麻烦。

按下 **Smart Step Into** (`Shift + F7`)，PyCharm 会高亮显示这行代码里的所有函数调用 (`calculate`, `get_modifier`, `process`)，你可以**直接点击**你想进入的那个函数！

### 2. 表达式求值 (Evaluate Expression)

在调试面板上方有一个计算器图标 🧮 (或者按 `Alt + F8` / `Option + F8`)。
这就打开了一个 Python Shell，环境就是当前暂停的上下文。
你可以：
- 执行任意代码：`user.calculate_age() + 10`
- 修改变量状态：`user.is_admin = True` (这会改变正在运行的程序！)

### 3. 行内值显示 (Inline Values)

你不需要去 Variables 面板找变量。PyCharm 会直接在编辑器代码行的末尾，用灰色文字显示该行变量的当前值。
`x = a + b  # x: 10`
一目了然。

---

## 🤖 AI 助手时间

> **Prompt**: "PyCharm 调试器中有一个功能叫 'Drop Frame' (丢弃帧)，它有什么作用？在 Python 中使用它有什么限制吗？"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 这是一个"后悔药"功能，能让你回退到函数调用的上一步，但 Python 对此的支持有限制，听听 AI 怎么说。

---

## ✅ 动手挑战

使用之前的 `exercise_02_01.py` (Buggy Calculator)。

**任务**：
1. 在 `result = str(a) + str(b)` 这一行设置断点。
2. 启动调试。
3. 当程序暂停时，使用 **Evaluate Expression** (`Alt+F8`)。
    - 输入 `a + b`，查看正确结果应该是多少。
    - 输入 `self.history`，查看当前历史记录。
4. 尝试使用 **Set Value** (在 Variables 面板右键变量) 将 `a` 的值在运行时修改为 `100`，然后继续运行 (`F9`)，观察输出结果的变化。

---

## 📝 总结

- **F8** (Over) 和 **F7** (Into) 是你的左右手。
- 遇到嵌套调用，记得用 **Smart Step Into** (`Shift + F7`)。
- **Evaluate Expression** 是实验和验证假设的最佳场所。
- PyCharm 的 **Inline Values** 让调试体验极其流畅。

下一章：我们将深入探讨 Python 的数据结构底层！
