# 模块 4-3 练习参考答案: 函数式数据清洗

users = [
    {"name": "Alice", "age": 25, "email": "alice@example.com"},
    {"name": "Bob", "age": 16, "email": "bob@gmail.com"},
    {"name": "Charlie", "age": 30, "email": "charlie@example.com"},
    {"name": "David", "age": 17, "email": "david@hotmail.com"}
]

# 步骤拆解版
# 1. 筛选成年人
adults = filter(lambda u: u["age"] >= 18, users)
# 2. 提取邮箱
emails = map(lambda u: u["email"], adults)
# 3. 转小写 (虽然示例已经是小写，但为了演示)
lower_emails = map(lambda e: e.lower(), emails)

print("Map/Filter 结果:", list(lower_emails))


# 列表推导式版 (Pythonic Way)
# 一行代码完成：筛选 -> 提取 -> 转换
processed_emails = [u["email"].lower() for u in users if u["age"] >= 18]

print("列表推导式结果:", processed_emails)
