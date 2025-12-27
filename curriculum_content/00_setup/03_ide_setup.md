# 模块 0-3: IDE 配置与解释器选择

## 🎯 学习目标

完成本节后，你将能够：
- 配置 VS Code 或 PyCharm 进行 Python 开发。
- **核心技能**: 在 IDE 中正确选择 Python 解释器 (Interpreter)。
- 安装并启用 GitHub Copilot。

---

## 🆚 方案 A: Visual Studio Code (推荐)

VS Code 是目前最流行的轻量级编辑器，插件生态极其丰富。

### 1. 安装插件
打开 VS Code，点击左侧扩展图标 (Extensions)，搜索并安装：
*   **Python** (Microsoft 出品)
*   **Pylance** (通常会自动安装，提供智能提示)
*   **GitHub Copilot**

### 2. 选择解释器 (Interpreter)
这是新手最容易踩坑的地方！**你必须告诉 VS Code 使用哪个 Python 来运行你的代码。**

1.  打开一个 Python 文件 (或者按 `Cmd+Shift+P` / `Ctrl+Shift+P` 打开命令面板)。
2.  输入并选择: `Python: Select Interpreter`。
3.  **关键**:
    *   如果你创建了虚拟环境 (`.venv`)，列表里应该会显示一个带 `('venv': venv)` 或类似标识的选项，**选它！**
    *   如果没有虚拟环境，选择标有 `Global` 或 `Recommended` 的系统 Python。

*状态栏确认*: VS Code 右下角会显示当前选中的 Python 版本。

### 3. 配置 Copilot
1.  安装 GitHub Copilot 插件后，右下角会提示登录 GitHub。
2.  登录并授权。
3.  确认右下角的 Copilot 图标是激活状态 (没有被划掉)。

---

## ⚙️ 方案 B: PyCharm (专业版/社区版)

PyCharm 是 JetBrains 出品的专业 Python IDE，功能强大但较重。

### 1. 配置解释器
1.  打开设置:
    *   **Windows**: `File` -> `Settings`
    *   **macOS**: `PyCharm` -> `Settings` (或 `Preferences`)
2.  导航到: `Project: <你的项目名>` -> `Python Interpreter`。
3.  点击右上角的齿轮图标 ⚙️ -> `Add...`。
4.  **选择环境**:
    *   **Existing environment**: 如果你已经用命令行创建了 `.venv`，选这个，然后找到 `.venv/bin/python` (macOS) 或 `.venv\Scripts\python.exe` (Windows)。
    *   **New environment**: 让 PyCharm 帮你创建一个新的虚拟环境。

### 2. 安装 Copilot
1.  在设置中导航到 `Plugins`。
2.  搜索 `GitHub Copilot` 并安装。
3.  重启 IDE 后登录 GitHub 账号。

---

## 🚀 验证配置

创建一个名为 `hello_ide.py` 的文件，输入：

```python
import sys

print("Hello, Python!")
print(f"当前使用的 Python 路径: {sys.executable}")
```

**运行它**:
*   **VS Code**: 点击右上角的 ▶️ 按钮。
*   **PyCharm**: 右键点击文件 -> `Run 'hello_ide'`.

**检查输出**:
看打印出来的路径是不是你预期的那个 (比如是不是在 `.venv` 目录下)。如果是，恭喜你，配置正确！

> 🤖 **AI 助手时间**:
> *   **Prompt**: "VS Code 的 settings.json 是做什么的？怎么在里面设置默认的 Python 路径？"
> *   **Action**: 询问 Copilot Chat。
> *   **Reflection**: 虽然界面操作很方便，但了解配置文件能让你更深入地掌控编辑器。
