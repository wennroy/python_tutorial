# 模块 0-1: Python 安装与版本管理

## 🎯 学习目标

完成本节后，你将能够：
- 理解 Python 解释器的作用。
- 在 Windows 或 macOS 上安装官方 Python。
- (可选) 安装 Anaconda 发行版。
- 找到不同系统下 Python 的安装路径。

---

## 🪝 引言：工欲善其事

在开始编写代码之前，我们需要先安装 "Python 解释器"。它就像是一个翻译官，把我们写的英文代码翻译成计算机能听懂的机器语言。

目前 Python 有两个主要版本流派：Python 2 (已停止维护) 和 Python 3。**本教程完全基于 Python 3.10+**。

---

## 📦 方案 A: 官方 Python 安装 (推荐轻量级用户)

这是最纯净的安装方式，适合大多数初学者。

### Windows 用户

1.  访问 [python.org/downloads](https://www.python.org/downloads/)。
2.  下载最新的 Python 3.10+ 安装包 (Installer)。
3.  **关键步骤**: 运行安装程序时，务必勾选底部的 **"Add Python to PATH"** (将 Python 添加到环境变量)。
    *   *如果不勾选，你在命令行里输入 `python` 时，电脑会说"找不到命令"。*
4.  点击 "Install Now"。

### macOS 用户

macOS 自带了 Python 2 (旧版) 或 Python 3 (Xcode 命令行工具)，但我们推荐使用 **Homebrew** 来管理，这样更干净、方便升级。

1.  打开终端 (Terminal)。
2.  检查是否安装了 Homebrew:
    ```bash
    brew --version
    ```
    如果没有，请访问 [brew.sh](https://brew.sh/) 获取安装命令。
3.  安装 Python:
    ```bash
    brew install python@3.11
    ```

---

## 🐍 方案 B: Anaconda 安装 (推荐数据科学/AI方向)

如果你未来的目标是数据分析、机器学习或深度学习，**Anaconda** 是一个非常强大的选择。它不仅包含了 Python，还预装了大量常用的数据科学库 (如 pandas, numpy) 和包管理器 conda。

1.  访问 [anaconda.com/download](https://www.anaconda.com/download)。
2.  下载对应系统的图形化安装包。
3.  按照提示安装。
    *   *注意*: Anaconda 可能会询问是否初始化 shell (conda init)，建议选择 "Yes"。

---

## 🔍 探秘：Python 到底装哪儿了？

了解 Python 的安装位置对于后续配置 IDE 非常重要。

### Windows 常见路径
*   **官方安装 (当前用户)**:
    `C:\Users\<你的用户名>\AppData\Local\Programs\Python\Python3xx\`
*   **Anaconda (当前用户)**:
    `C:\Users\<你的用户名>\anaconda3\` 或 `C:\ProgramData\Anaconda3\`

### macOS 常见路径
*   **Homebrew**:
    `/opt/homebrew/bin/python3` (Apple Silicon) 或 `/usr/local/bin/python3` (Intel)
*   **Anaconda**:
    `/Users/<你的用户名>/anaconda3/bin/python`
*   **系统自带 (不要乱动)**:
    `/usr/bin/python3`

### 如何自己查找？
在终端或命令行中输入：

*   **Windows**: `where python`
*   **macOS/Linux**: `which python3`

---

## ✅ 验证安装

打开你的终端 (Terminal) 或 命令提示符 (cmd/PowerShell)，输入：

```bash
python --version
# 或者
python3 --version
```

如果看到了类似 `Python 3.11.x` 的输出，恭喜你，第一步完成了！

> 🤖 **AI 助手时间**:
> *   **Prompt**: "Windows 环境变量 PATH 是什么？为什么要把它加进去？"
> *   **Action**: 询问 Copilot Chat。
> *   **Reflection**: 想象一下，如果没有 PATH，每次运行 Python 都要输入完整路径 `C:\Users\...\python.exe`，是不是很麻烦？
