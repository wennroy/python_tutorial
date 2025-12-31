# 第三章：requests 库与 HTTP 请求

> 🎯 **学习目标**
> - 掌握 HTTP 协议基础知识
> - 熟练使用 requests 库发送各种 HTTP 请求
> - 学会处理响应、错误和超时
> - 了解会话管理和高级用法

---

## 1. 引言：为什么需要 HTTP 请求？

现代应用很少单打独斗：
- 🌐 **调用第三方 API**：天气、地图、支付
- 🤖 **调用 AI 服务**：OpenAI、Claude、本地模型
- 📊 **数据采集**：爬虫、数据同步
- 🔗 **微服务通信**：服务间调用

`requests` 是 Python 最流行的 HTTP 库，简单易用。

```bash
pip install requests
```

---

## 2. HTTP 协议基础

### 2.1 HTTP 请求方法

| 方法 | 用途 | 幂等性 | 示例 |
|-----|------|--------|------|
| GET | 获取资源 | ✅ | 查询用户列表 |
| POST | 创建资源 | ❌ | 创建新用户 |
| PUT | 完整更新 | ✅ | 更新用户信息 |
| PATCH | 部分更新 | ✅ | 修改用户邮箱 |
| DELETE | 删除资源 | ✅ | 删除用户 |

### 2.2 HTTP 状态码

```python
# 2xx 成功
200  # OK - 请求成功
201  # Created - 资源创建成功
204  # No Content - 成功但无返回内容

# 3xx 重定向
301  # Moved Permanently - 永久重定向
302  # Found - 临时重定向

# 4xx 客户端错误
400  # Bad Request - 请求格式错误
401  # Unauthorized - 未认证
403  # Forbidden - 无权限
404  # Not Found - 资源不存在
429  # Too Many Requests - 请求过多（限流）

# 5xx 服务器错误
500  # Internal Server Error - 服务器内部错误
502  # Bad Gateway - 网关错误
503  # Service Unavailable - 服务不可用
```

---

## 3. requests 基础用法

### 3.1 GET 请求

```python
import requests

# 简单 GET 请求
response = requests.get("https://api.github.com/users/octocat")

# 检查状态
print(response.status_code)  # 200
print(response.ok)           # True (status_code < 400)

# 获取响应内容
print(response.text)         # 字符串
print(response.json())       # 解析为字典
print(response.content)      # 二进制内容

# 响应头
print(response.headers['Content-Type'])  # application/json
```

### 3.2 带参数的 GET 请求

```python
# 方式 1: 手动拼接 URL
response = requests.get("https://api.example.com/search?q=python&page=1")

# 方式 2: 使用 params 参数（推荐）
params = {
    "q": "python",
    "page": 1,
    "sort": "stars"
}
response = requests.get("https://api.github.com/search/repositories", params=params)

# 实际请求的 URL
print(response.url)  # https://api.github.com/search/repositories?q=python&page=1&sort=stars
```

### 3.3 POST 请求

```python
# 发送 JSON 数据（最常用）
data = {
    "name": "张三",
    "email": "zhangsan@example.com"
}
response = requests.post(
    "https://api.example.com/users",
    json=data  # 自动设置 Content-Type: application/json
)

# 发送表单数据
form_data = {
    "username": "zhangsan",
    "password": "secret123"
}
response = requests.post(
    "https://api.example.com/login",
    data=form_data  # Content-Type: application/x-www-form-urlencoded
)

# 上传文件
files = {
    "file": open("document.pdf", "rb"),
    # 或者指定文件名和类型
    # "file": ("document.pdf", open("document.pdf", "rb"), "application/pdf")
}
response = requests.post("https://api.example.com/upload", files=files)
```

### 3.4 其他 HTTP 方法

```python
# PUT - 完整更新
response = requests.put(
    "https://api.example.com/users/123",
    json={"name": "李四", "email": "lisi@example.com"}
)

# PATCH - 部分更新
response = requests.patch(
    "https://api.example.com/users/123",
    json={"email": "new_email@example.com"}
)

# DELETE - 删除
response = requests.delete("https://api.example.com/users/123")
```

---

## 4. 请求头与认证

### 4.1 自定义请求头

```python
headers = {
    "User-Agent": "MyApp/1.0",
    "Accept": "application/json",
    "X-Custom-Header": "custom-value"
}
response = requests.get("https://api.example.com/data", headers=headers)
```

### 4.2 认证方式

```python
# 方式 1: Bearer Token（最常用）
headers = {
    "Authorization": "Bearer your-api-key-here"
}
response = requests.get("https://api.openai.com/v1/models", headers=headers)

# 方式 2: Basic Auth
from requests.auth import HTTPBasicAuth
response = requests.get(
    "https://api.example.com/protected",
    auth=HTTPBasicAuth("username", "password")
)
# 或简写
response = requests.get(
    "https://api.example.com/protected",
    auth=("username", "password")
)

# 方式 3: API Key 作为参数
response = requests.get(
    "https://api.example.com/data",
    params={"api_key": "your-api-key"}
)
```

---

## 5. 错误处理与超时

### 5.1 超时设置

```python
# 设置超时（秒）
try:
    response = requests.get(
        "https://api.example.com/slow-endpoint",
        timeout=5  # 5 秒超时
    )
except requests.exceptions.Timeout:
    print("请求超时！")

# 分别设置连接超时和读取超时
response = requests.get(
    "https://api.example.com/data",
    timeout=(3, 10)  # 连接超时 3 秒，读取超时 10 秒
)
```

### 5.2 完整的错误处理

```python
import requests
from requests.exceptions import (
    RequestException,
    ConnectionError,
    Timeout,
    HTTPError
)

def fetch_data(url: str) -> dict | None:
    """安全地获取数据"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 4xx/5xx 会抛出 HTTPError
        return response.json()
    
    except ConnectionError:
        print(f"连接失败: {url}")
    except Timeout:
        print(f"请求超时: {url}")
    except HTTPError as e:
        print(f"HTTP 错误: {e.response.status_code}")
        if e.response.status_code == 404:
            print("资源不存在")
        elif e.response.status_code == 401:
            print("认证失败")
        elif e.response.status_code == 429:
            print("请求过于频繁，请稍后重试")
    except RequestException as e:
        print(f"请求异常: {e}")
    
    return None
```

### 5.3 重试机制

```python
import time
from typing import Callable

def retry_request(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0
) -> requests.Response | None:
    """带重试的请求"""
    for attempt in range(max_retries):
        try:
            response = func()
            response.raise_for_status()
            return response
        except (requests.exceptions.RequestException) as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay * (backoff ** attempt)
            print(f"请求失败，{wait_time}秒后重试... ({attempt + 1}/{max_retries})")
            time.sleep(wait_time)
    return None

# 使用
response = retry_request(
    lambda: requests.get("https://api.example.com/data", timeout=5)
)
```

---

## 6. Session 会话管理

### 6.1 为什么使用 Session？

```python
# 不使用 Session：每次请求都是独立的
requests.get("https://api.example.com/data1")  # 新连接
requests.get("https://api.example.com/data2")  # 新连接

# 使用 Session：复用连接，更高效
with requests.Session() as session:
    session.get("https://api.example.com/data1")  # 复用连接
    session.get("https://api.example.com/data2")  # 复用连接
```

### 6.2 Session 的优势

```python
session = requests.Session()

# 1. 设置全局请求头
session.headers.update({
    "Authorization": "Bearer your-token",
    "User-Agent": "MyApp/1.0"
})

# 2. 自动处理 Cookies
session.post("https://api.example.com/login", data={"user": "admin", "pass": "123"})
# 后续请求自动带上登录后的 Cookie
session.get("https://api.example.com/protected")

# 3. 复用 TCP 连接，提高性能
for i in range(100):
    session.get(f"https://api.example.com/item/{i}")

# 记得关闭
session.close()

# 或使用上下文管理器（推荐）
with requests.Session() as session:
    session.headers["Authorization"] = "Bearer token"
    response = session.get("https://api.example.com/data")
```

---

## 7. 实战案例

### 7.1 调用 OpenAI API

```python
import requests

def call_openai(prompt: str, api_key: str) -> str:
    """调用 OpenAI ChatGPT API"""
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

# 使用
answer = call_openai("Python 的优点是什么？", "sk-your-api-key")
print(answer)
```

### 7.2 GitHub API 封装

```python
class GitHubClient:
    """GitHub API 客户端"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str = None):
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/vnd.github+json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    
    def get_user(self, username: str) -> dict:
        """获取用户信息"""
        response = self.session.get(f"{self.BASE_URL}/users/{username}")
        response.raise_for_status()
        return response.json()
    
    def get_repos(self, username: str) -> list:
        """获取用户的仓库列表"""
        response = self.session.get(
            f"{self.BASE_URL}/users/{username}/repos",
            params={"sort": "updated", "per_page": 10}
        )
        response.raise_for_status()
        return response.json()
    
    def search_repos(self, query: str, language: str = None) -> list:
        """搜索仓库"""
        q = query
        if language:
            q += f" language:{language}"
        
        response = self.session.get(
            f"{self.BASE_URL}/search/repositories",
            params={"q": q, "sort": "stars", "per_page": 10}
        )
        response.raise_for_status()
        return response.json()["items"]
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

# 使用
with GitHubClient() as client:
    user = client.get_user("torvalds")
    print(f"Linus Torvalds has {user['public_repos']} public repos")
    
    repos = client.search_repos("machine learning", language="python")
    for repo in repos[:5]:
        print(f"- {repo['full_name']} ⭐ {repo['stargazers_count']}")
```

---

## 8. 高级技巧

### 8.1 流式下载大文件

```python
def download_file(url: str, filename: str):
    """流式下载大文件，避免内存溢出"""
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                # 显示进度
                if total_size:
                    progress = downloaded / total_size * 100
                    print(f"\r下载进度: {progress:.1f}%", end="")
    
    print("\n下载完成！")
```

### 8.2 代理设置

```python
proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "http://proxy.example.com:8080",
}

response = requests.get("https://api.example.com/data", proxies=proxies)

# 或在 Session 中设置
session = requests.Session()
session.proxies = proxies
```

### 8.3 SSL 证书处理

```python
# 跳过 SSL 验证（不推荐，仅用于调试）
response = requests.get("https://self-signed.example.com", verify=False)

# 使用自定义证书
response = requests.get("https://api.example.com", verify="/path/to/cert.pem")
```

---

## 9. 动手练习

### 练习 1：天气查询 API

```python
# 使用 wttr.in API 查询天气
def get_weather(city: str) -> str:
    """查询城市天气"""
    # 提示：wttr.in 支持中文城市名
    # URL 格式: https://wttr.in/{city}?format=3
    pass

# 测试
print(get_weather("Beijing"))
print(get_weather("上海"))
```

### 练习 2：封装 REST API 客户端

```python
# 为 JSONPlaceholder (https://jsonplaceholder.typicode.com) 创建客户端
class JSONPlaceholderClient:
    """REST API 客户端练习"""
    
    def list_posts(self) -> list:
        """获取所有帖子"""
        pass
    
    def get_post(self, post_id: int) -> dict:
        """获取单个帖子"""
        pass
    
    def create_post(self, title: str, body: str, user_id: int) -> dict:
        """创建帖子"""
        pass
    
    def delete_post(self, post_id: int) -> bool:
        """删除帖子"""
        pass
```

---

## 10. 小结

| 功能 | 方法/参数 |
|-----|----------|
| GET 请求 | `requests.get(url, params=...)` |
| POST 请求 | `requests.post(url, json=..., data=...)` |
| 请求头 | `headers={...}` |
| 超时 | `timeout=5` 或 `timeout=(3, 10)` |
| Session | `with requests.Session() as s:` |
| 错误处理 | `response.raise_for_status()` |
| 流式下载 | `stream=True` + `iter_content()` |

---

> 🤖 **AI 助手时间**
> 
> - **Prompt**: "帮我封装一个调用 OpenAI API 的类，支持重试和流式输出"
> - **Prompt**: "这个 API 调用代码有什么问题？帮我优化错误处理"
