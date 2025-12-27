# exercise_01_06.py - Reference Solution
# 参考答案

from datetime import datetime, timedelta, date
# 注意：zoneinfo 需要 Python 3.9+
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # 如果版本过低，可以使用 pytz (需要 pip install pytz)
    # 这里为了演示简单，假设环境是 3.9+
    print("Warning: zoneinfo not found, please use Python 3.9+")
    ZoneInfo = None

# 1. 生日倒计时
def days_until_birthday(month, day):
    today = date.today()
    # 假设今年的生日
    this_year_bday = date(today.year, month, day)
    
    if this_year_bday < today:
        # 如果今年已经过了，就算明年的
        next_bday = date(today.year + 1, month, day)
    else:
        next_bday = this_year_bday
        
    diff = next_bday - today
    return diff.days


# 2. 会议调度器
def schedule_meeting():
    if ZoneInfo is None:
        return
        
    # UTC 时间
    utc_time = datetime(2023, 11, 11, 14, 0, tzinfo=ZoneInfo("UTC"))
    
    cities = [
        "America/Los_Angeles",
        "America/New_York",
        "Europe/London",
        "Asia/Shanghai",
        "Asia/Tokyo"
    ]
    
    print(f"Meeting Time (UTC): {utc_time}")
    for city in cities:
        local_time = utc_time.astimezone(ZoneInfo(city))
        print(f"{city:<20}: {local_time.strftime('%Y-%m-%d %H:%M')}")


# 3. 工作日计算器
def add_business_days(start_date, days_to_add):
    current_date = start_date
    added = 0
    while added < days_to_add:
        current_date += timedelta(days=1)
        # weekday(): 0=Mon, 6=Sun. < 5 means Mon-Fri
        if current_date.weekday() < 5:
            added += 1
    return current_date


# 测试代码
if __name__ == "__main__":
    # 测试 1
    # 假设生日是 12月25日
    days = days_until_birthday(12, 25)
    print(f"Days until birthday: {days}")
    
    # 测试 2
    print("\n--- World Meeting Schedule ---")
    schedule_meeting()
    
    # 测试 3
    print("\n--- Business Days ---")
    today = date.today()
    future_date = add_business_days(today, 10)
    print(f"10 business days from {today} is {future_date}")
