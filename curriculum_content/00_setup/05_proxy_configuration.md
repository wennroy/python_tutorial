# 模块 0-5: 网络代理配置指南 (Proxy Configuration)

## 🎯 学习目标

完成本节后，你将能够：
- 理解代理服务器 (Proxy Server) 的工作原理。
- 在不同操作系统终端 (Bash, CMD, PowerShell) 中配置代理。
- 为开发工具 (pip, git, conda) 设置代理。
- 在 Python 代码 (`requests`) 中处理代理请求。

---

## 🕵️‍♂️ 引言：什么是代理服务器？

在公司网络或特定网络环境下，你可能无法直接访问外部互联网（如 GitHub, PyPI, Google）。这时，你需要一个"中间人"来帮你传递数据，这个中间人就是 **代理服务器 (Proxy Server)**。

### 原理图解

*   **无代理**: 你的电脑 ➡️ 目标网站 (被墙/无法连接 ❌)
*   **有代理**: 你的电脑 ➡️ **代理服务器** ➡️ 目标网站 (成功 ✅)

代理服务器接收你的请求，代表你去访问目标网站，然后把结果传回给你。

---

## 💻 终端环境配置 (Terminal)

很多开发工具（如 curl, wget, brew）都依赖终端的环境变量来决定是否走代理。

### 1. macOS / Linux (Bash, Zsh)

在终端中临时设置（关闭终端后失效）：
```bash
export http_proxy="http://proxy.example.com:8080"
export https_proxy="http://proxy.example.com:8080"
# 如果有不需要走代理的内网地址
export no_proxy="localhost,127.0.0.1,.mycompany.com"
```

永久生效（写入 `~/.zshrc` 或 `~/.bashrc`）：
```bash
echo 'export http_proxy="http://proxy.example.com:8080"' >> ~/.zshrc
echo 'export https_proxy="http://proxy.example.com:8080"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Windows (CMD)

```cmd
set http_proxy=http://proxy.example.com:8080
set https_proxy=http://proxy.example.com:8080
```

### 3. Windows (PowerShell)

```powershell
$env:http_proxy="http://proxy.example.com:8080"
$env:https_proxy="http://proxy.example.com:8080"
```

---

## 🛠️ 开发工具配置

即使设置了环境变量，有些工具可能需要单独配置。

### 1. pip (Python 包管理器)

如果下载包很慢或超时，可以尝试：

**临时使用**:
```bash
pip install pandas --proxy http://proxy.example.com:8080
```

**永久配置** (`pip.ini` 或 `pip.conf`):
```ini
[global]
proxy = http://proxy.example.com:8080
```

### 2. Git (版本控制)

无法 `git clone` 或 `git push` 时：

```bash
# 设置全局代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# 取消代理
git config --global --unset http.proxy
```

### 3. Conda

修改用户目录下的 `.condarc` 文件：

```yaml
proxy_servers:
  http: http://proxy.example.com:8080
  https: http://proxy.example.com:8080
```

---

## 🐍 代码实战：在 Python 中使用代理

在编写爬虫或调用 API 时，你可能需要在代码层面控制代理。

### 场景 A: 自动读取环境变量 (默认行为)
Python 的 `requests` 库非常智能，它会自动读取系统环境变量 (`HTTP_PROXY`, `HTTPS_PROXY`)。如果你在终端设置好了，直接运行代码通常就能生效。

### 场景 B: 代码中显式指定 (requests)

如果你想在代码里强制指定代理，或者针对不同请求使用不同代理：

```python
import requests

# 定义代理字典
proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "http://proxy.example.com:8080",
}

try:
    # 访问 Google，显式传入 proxies 参数
    response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
    print(f"状态码: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

### 场景 C: 带有认证的代理
如果你的公司代理需要用户名和密码：

```python
proxies = {
    "http": "http://user:password@proxy.example.com:8080",
    "https": "http://user:password@proxy.example.com:8080",
}
```

> 🤖 **AI 助手时间**:
> *   **Prompt**: "如何用 Python 检查当前的环境变量里有没有设置代理？"
> *   **Action**: 询问 Copilot Chat。
> *   **Reflection**: 提示：可以使用 `os.environ.get('http_proxy')`。
