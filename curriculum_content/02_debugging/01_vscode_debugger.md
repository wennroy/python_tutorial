# 模块 2: 调试艺术 - VS Code 调试器入门

## 🎯 学习目标

完成本章后，你将能够：
- 告别 `print()` 调试法，拥抱专业的 IDE 调试器
- 理解并配置 `launch.json`
- 熟练使用断点 (Breakpoints)、步进 (Step Over/Into/Out)
- 使用变量监视 (Watch) 和调用堆栈 (Call Stack) 定位问题

---

## 🪝 引言：福尔摩斯的放大镜

想象一下，你是一个侦探，正在调查一起"程序崩溃"的谋杀案。
`print()` 就像是你在现场随机拍照，希望能拍到线索。
而**调试器 (Debugger)** 就像是让时间静止，你可以走到嫌疑人面前，翻看他的口袋，甚至倒带重来。

VS Code 内置了世界级的 Python 调试器，今天我们就来学会使用它。

---

## 🧠 核心概念：调试器的基本操作

### 1. 启动调试 (Launch)

首先，你需要告诉 VS Code 如何运行你的代码。通常，直接按 `F5` 即可。
如果需要自定义参数，可以创建 `.vscode/launch.json` 文件：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

### 2. 断点 (Breakpoints) 🔴

在行号左侧点击，会出现一个红点。程序运行到这里会**暂停**。

### 3. 控制条 (Debug Toolbar)

当程序暂停时，顶部会出现一个控制条：

- **▶️ 继续 (Continue / F5)**: 运行直到下一个断点。
- **↷ 单步跳过 (Step Over / F10)**: 运行下一行代码。如果这行是函数调用，**不进入**函数内部，直接获取结果。
- **⬇️ 单步调试 (Step Into / F11)**: 如果这行是函数调用，**进入**函数内部。
- **⬆️ 单步跳出 (Step Out / Shift+F11)**: 执行完当前函数剩余代码，返回到调用它的地方。
- **🔄 重启 (Restart / Cmd+Shift+F5)**: 重新开始调试。
- **⏹️ 停止 (Stop / Shift+F5)**: 终止程序。

*(注：Windows/Linux 下快捷键可能略有不同，请以菜单显示为准)*

---

## 🕵️‍♂️ 侦探工具箱

### 1. 变量 (Variables) 面板
左侧栏会自动显示当前作用域内的所有变量及其值。你可以直接双击修改它们的值来测试不同情况！

### 2. 监视 (Watch) 面板
如果你关心某个复杂的表达式（例如 `user.address.zipcode`），可以把它添加到 Watch 面板，实时监控它的变化。

### 3. 调用堆栈 (Call Stack)
显示了"我是怎么来到这里的"。
例如：`main()` -> `process_data()` -> `calculate_sum()`。
点击堆栈中的不同层级，可以查看那一层的变量状态。

---

## 🤖 AI 助手时间

> **Prompt**: "解释 VS Code 调试配置 `launch.json` 中 `justMyCode: true` 的作用是什么？如果我想调试第三方库的代码该怎么办？"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 这是一个非常实用的配置，特别是当你怀疑 Bug 出在引用的库里时。

---

## ✅ 动手挑战

我们将提供一个名为 `buggy_calculator.py` 的文件（见练习文件）。它包含一个简单的计算器类，但有很多 Bug。

**任务**：
1. 在 `add` 方法中设置断点。
2. 使用 `F11` (Step Into) 进入 `add` 方法。
3. 观察变量面板，找出为什么 `1 + 1` 竟然等于 `11`？
4. 修复它。

```python
# 示例代码片段
class Calculator:
    def add(self, a, b):
        return str(a) + str(b) # 哎呀，这里好像有问题...
```

---

## 📝 总结

- **断点**让程序暂停。
- **Step Over** 看结果，**Step Into** 看细节。
- **Call Stack** 告诉你程序的执行路径。
- 别再满屏打 `print` 了，用调试器吧！

下一章：高级调试技巧——让调试更智能！
