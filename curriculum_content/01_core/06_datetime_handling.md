# 模块 1: Python 核心强化 - 时间与日期的掌控

## 🎯 学习目标

完成本章后，你将能够：
- 区分 `date`, `time`, `datetime` 对象
- 熟练进行时间格式化与解析 (`strftime` vs `strptime`)
- 使用 `timedelta` 进行时间加减运算
- 理解并处理时区 (Timezone) 问题

---

## 🪝 引言：跨时区的会议

你的服务器在伦敦 (UTC)，你的用户在北京 (UTC+8)，而你的老板在纽约 (UTC-5)。
当用户说"明天早上 9 点开会"时，到底是哪个"明天"？

时间处理是软件开发中最大的坑之一。Python 的 `datetime` 模块是你的救生圈。

---

## 🧠 核心概念：datetime 家族

```python
from datetime import datetime, date, time, timedelta

# 获取当前时间
now = datetime.now()
print(f"现在: {now}")

# 获取日期部分
today = date.today()
print(f"今天: {today}")

# 构建特定时间
meeting = datetime(2023, 12, 25, 10, 30) # 2023-12-25 10:30:00
```

### 1. 时间运算：timedelta

想要知道 100 天后是几号？或者计算两个时间点差了多久？

```python
# 时间推移
future = now + timedelta(days=100, hours=2)
print(f"100天2小时后: {future}")

# 时间差计算
diff = future - now
print(f"相差秒数: {diff.total_seconds()}")
```

### 2. 格式化：字符串 <-> 时间对象

- **`strftime` (String Format Time)**: 对象 -> 字符串
- **`strptime` (String Parse Time)**: 字符串 -> 对象

记忆口诀：**f** for **Format** (出去), **p** for **Parse** (进来)。

```python
# 格式化输出
print(now.strftime("%Y-%m-%d %H:%M:%S")) # 2023-10-01 12:00:00

# 解析字符串
log_time = "2023/10/01 14:30"
dt = datetime.strptime(log_time, "%Y/%m/%d %H:%M")
```

---

## 🌍 进阶：时区 (Timezone)

Python 3.9+ 引入了 `zoneinfo` 库，终于让时区处理变得简单了。
*注意：Windows 上可能需要安装 `tzdata` 包 (`pip install tzdata`)。*

```python
from zoneinfo import ZoneInfo

# 创建带时区的时间 (Aware Datetime)
utc_now = datetime.now(ZoneInfo("UTC"))
beijing_now = utc_now.astimezone(ZoneInfo("Asia/Shanghai"))

print(f"UTC: {utc_now}")
print(f"北京: {beijing_now}")
```

**最佳实践**：
1. 在数据库和内部逻辑中，永远存储 **UTC** 时间。
2. 只在展示给用户时，才转换为用户的本地时区。

---

## 🤖 AI 助手时间

> **Prompt**: "帮我写一个 Python 函数，输入一个 Unix 时间戳 (Timestamp)，将其转换为 'YYYY-MM-DD HH:MM:SS' 格式的北京时间字符串。"
> 
> **Action**: 唤起 Copilot Chat。
> 
> **Reflection**: 看看 AI 是否使用了 `fromtimestamp` 方法？它处理时区了吗？

---

## ✅ 动手挑战

创建文件 `exercise_01_06.py`，完成以下任务：

```python
# 1. 生日倒计时
#    输入你的生日（月和日），计算距离下一个生日还有多少天、多少小时。

# 2. 会议调度器
#    假设有一个全球会议要在 UTC 时间 2023-11-11 14:00 召开。
#    请列出以下城市的本地会议时间：
#    - Los Angeles (America/Los_Angeles)
#    - New York (America/New_York)
#    - London (Europe/London)
#    - Beijing (Asia/Shanghai)
#    - Tokyo (Asia/Tokyo)

# 3. 工作日计算器
#    计算从今天开始往后数 10 个工作日（周一到周五）是哪一天。
#    提示：使用 while 循环和 timedelta，判断 weekday()。
```

---

## 📝 总结

- `datetime` 是核心类，`timedelta` 用于计算。
- 牢记 `strftime` (对象转字符串) 和 `strptime` (字符串转对象)。
- 处理跨国业务时，**UTC 是唯一的真理**，`zoneinfo` 是你的好帮手。

恭喜！你已经掌握了 Python 核心模块中最实用的部分。
