# 模块 0-2: 虚拟环境 (Virtual Environments)

## 🎯 学习目标

完成本节后，你将能够：
- 理解为什么需要虚拟环境。
- 使用 `venv` 创建和激活虚拟环境。
- (可选) 使用 `conda` 管理环境。

---

## 🪝 引言：为什么需要"分身"？

想象一下，你正在开发两个项目：
*   **项目 A**: 一个老旧的网站，依赖 `Django 2.0`。
*   **项目 B**: 一个全新的 AI 应用，依赖 `Django 4.0`。

如果你把所有库都装在同一个 Python 里 (全局环境)，`Django 2.0` 和 `4.0` 会打架 (版本冲突)。

**虚拟环境** 就像是给每个项目分配了一个独立的"沙盒"。项目 A 在沙盒 A 里玩，项目 B 在沙盒 B 里玩，互不干扰。

---

## 🛠️ 方案 A: 使用 venv (Python 自带)

这是 Python 标准库自带的工具，轻量、通用。

### 1. 创建环境
在你的项目文件夹下打开终端：

```bash
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```
*这会在当前目录下创建一个名为 `.venv` 的文件夹，里面包含了一个独立的 Python 解释器。*

### 2. 激活环境
激活后，你的终端提示符通常会变样，前面多一个 `(.venv)`。

*   **Windows (cmd)**:
    ```cmd
    .venv\Scripts\activate.bat
    ```
*   **Windows (PowerShell)**:
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
    *(如果报错"禁止运行脚本"，请以管理员身份运行 PowerShell 并输入 `Set-ExecutionPolicy RemoteSigned`)*
*   **macOS / Linux**:
    ```bash
    source .venv/bin/activate
    ```

### 3. 退出环境
```bash
deactivate
```

---

## 🐍 方案 B: 使用 Conda (Anaconda/Miniconda)

如果你安装了 Anaconda，Conda 是一个更强大的环境管理工具，它不仅能管 Python 包，还能管非 Python 的依赖 (比如 C++ 库)。

### 1. 创建环境
```bash
# 创建一个名为 myenv 的环境，指定 Python 版本为 3.10
conda create -n myenv python=3.10
```

### 2. 激活环境
```bash
conda activate myenv
```

### 3. 列出所有环境
```bash
conda env list
```

---

## 📦 包管理基础 (pip)

`pip` 是 Python 的标准包管理工具。在虚拟环境中，我们使用它来安装、升级和卸载第三方库。

### 常用指令

```bash
# 1. 安装库
pip install pandas          # 安装最新版
pip install pandas==2.0.0   # 安装指定版本 (非常重要！)
pip install --upgrade pandas # 升级到最新版

# 2. 卸载库
pip uninstall pandas

# 3. 查看已安装的库
pip list
pip show pandas             # 查看特定库的详细信息 (版本、安装位置、依赖)

# 4. 依赖管理 (团队协作必备)
# 将当前环境所有包导出到文件
pip freeze > requirements.txt

# 根据文件一键安装所有包
pip install -r requirements.txt
```

### 💡 最佳实践
*   **永远在虚拟环境中操作**：避免污染全局 Python 环境。
*   **使用国内镜像源** (如果下载速度慢)：
    ```bash
    pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

---

## ⚡️ 进阶：极速包管理 (uv)

[uv](https://github.com/astral-sh/uv) 是一个用 Rust 编写的超快速 Python 包安装器和解析器。它的速度通常比 pip 快 10-100 倍，正在成为 Python 社区的新宠。

### 1. 安装 uv
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者直接用 pip 安装
pip install uv
```

### 2. 使用 uv 替代 pip
`uv` 的命令设计得与 `pip` 非常相似，迁移成本极低。

```bash
# 创建虚拟环境 (比 python -m venv 快得多)
uv venv

# 激活环境 (同上)
# source .venv/bin/activate  (macOS/Linux)
# .venv\Scripts\activate     (Windows)

# 安装包
uv pip install pandas
uv pip install -r requirements.txt

# 同步环境 (确保环境与 requirements.txt 完全一致，多余的包会被删除)
uv pip sync requirements.txt
```

### 为什么选择 uv?
*   **速度**: 极快的依赖解析和下载速度。
*   **确定性**: `uv pip sync` 能确保你的环境和定义文件完全一致，治愈"我的电脑上能跑"的顽疾。

> 🤖 **AI 助手时间**:
> *   **Prompt**: "解释一下 `pip install` 和 `conda install` 的区别是什么？"
> *   **Action**: 询问 Copilot Chat。
> *   **Reflection**: 它们虽然都是装包的，但背后的仓库源和解决依赖冲突的能力有所不同哦。
