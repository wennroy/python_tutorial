# 模块 Extra: 专业级日志记录 (Logging)

## 🎯 学习目标

完成本章后，你将能够：
- 理解标准流 (`stdin`, `stdout`, `stderr`) 的区别
- 掌握 Python `logging` 模块的层级与配置
- 学会自定义日志格式 (Formatter)
- 实现将日志同时输出到控制台和文件

---

## 🪝 引言：为什么 print() 还不够？

在开发阶段，`print("Here!")` 确实很方便。但在生产环境中，它就是一场灾难：
1.  **无法关闭**：上线后满屏的调试信息，想关掉只能改代码。
2.  **信息匮乏**：不知道是几点发生的，也不知道是哪个模块出的错。
3.  **无法分类**：普通的提示信息和严重的系统崩溃混在一起。

这时候，你需要专业的 **Logging** 系统。

---

## 🧠 核心概念：标准流与日志层级

### 1. 标准流 (Standard Streams)

在操作系统层面，每个程序启动时都会自动连接三个"管道"：

*   **stdin (Standard Input)**: 标准输入。通常是键盘输入。
*   **stdout (Standard Output)**: 标准输出。`print()` 默认输出到这里。通常显示在终端屏幕上。
*   **stderr (Standard Error)**: 标准错误。专门用于输出错误信息。

**为什么区分 stdout 和 stderr？**
你可以把它们重定向到不同的地方。例如，把正常的输出存入 `output.txt`，把错误信息存入 `error.log`。

### 2. 日志层级 (Logging Levels)

Python 定义了 5 个标准的日志级别，严重程度递增：

| 级别 | 数值 | 适用场景 |
| :--- | :--- | :--- |
| **DEBUG** | 10 | 只有开发者关心的细节（变量值、循环进度）。 |
| **INFO** | 20 | 确认程序按预期运行（"服务已启动"、"用户登录"）。 |
| **WARNING** | 30 | ⚠️ 默认级别。有些意外发生，但程序还能跑（"磁盘空间不足"）。 |
| **ERROR** | 40 | 更严重的问题，某些功能无法执行（"数据库连接失败"）。 |
| **CRITICAL** | 50 | 严重错误，程序可能即将崩溃。 |

---

## ⚙️ 实战：配置你的 Logger

### 1. 基础配置 (Basic Config)

最简单的用法，适合脚本。

```python
import logging

# 配置日志级别和格式
logging.basicConfig(
    level=logging.INFO, # 设置最低显示级别
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.debug("这条看不见，因为级别不够")
logging.info("程序启动了")
logging.warning("注意！")
logging.error("出错了！")
```

### 2. 进阶配置：Handler 与 Formatter

如果你想**同时**把日志打印到屏幕（stdout）并保存到文件，就需要更高级的配置。

*   **Logger**: 记录器，程序的入口。
*   **Handler**: 处理器，决定日志去哪（控制台、文件、邮件...）。
*   **Formatter**: 格式化器，决定日志长什么样。

```python
import logging
import sys

# 1. 创建 Logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG) # 总开关

# 2. 创建 Handler
# 输出到控制台 (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO) # 控制台只看 INFO 以上

# 输出到文件
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG) # 文件记录所有细节

# 3. 创建 Formatter
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s'
)

# 4. 组装
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 5. 使用
logger.info("这条会同时出现在屏幕和文件里")
logger.debug("这条只会出现在文件里")
```

---

## 🤖 AI 助手时间

> **Prompt**: "帮我写一个 Python logging 配置，使用 `RotatingFileHandler`。要求：日志文件名为 `server.log`，最大 5MB，最多保留 3 个备份。并解释为什么在长期运行的服务中需要这样做。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 看看 AI 是否解释了"日志轮转" (Log Rotation) 的概念？这对于防止磁盘被日志填满至关重要。

---

## ✅ 动手挑战

创建文件 `exercise_extra_03.py`，完成以下任务：

```python
# 1. 模拟电商系统日志
#    创建一个 Logger，名为 "ecommerce"。
#    配置两个 Handler：
#    - StreamHandler: 输出 WARNING 及以上级别到控制台。
#    - FileHandler: 输出 INFO 及以上级别到 "orders.log"。
#    
#    模拟以下场景并记录日志：
#    - INFO: 用户 "Alice" 下单成功，订单号 #1001
#    - WARNING: 库存不足，商品 ID 888 仅剩 2 件
#    - ERROR: 支付网关超时，订单 #1002 支付失败

# 2. 格式化挑战
#    修改 Formatter，使其输出格式包含：时间戳、日志级别、文件名、行号、消息。
#    提示：查找 Python logging LogRecord attributes 文档，找到文件名和行号的占位符。
```

---

## 📝 总结

- **stdout/stderr** 是程序与外界沟通的管道。
- **Logging** 模块通过 **Level** 控制信息的繁简。
- 使用 **Handler** 可以灵活地将日志分发到不同目的地。
- 生产环境中，务必配置 **Log Rotation** 以免撑爆硬盘。

下一章：我们将探索 Python 的并发编程世界！
