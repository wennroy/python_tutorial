# exercise_01_04.py - Reference Solution
# 参考答案

import re

# 1. 敏感词过滤
def censor_text(text, sensitive_words):
    """
    将 text 中的敏感词替换为 "*"
    """
    # 简单的循环替换
    # for word in sensitive_words:
    #     text = text.replace(word, "*" * len(word))
    
    # 进阶：使用正则忽略大小写
    for word in sensitive_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("*" * len(word), text)
        
    return text


# 2. 日志解析器
def parse_log(log_text):
    """
    提取出所有的日志级别（INFO, ERROR）和时间戳。
    """
    # 模式：日期 时间 [级别]
    # 2023-10-01 10:00:01 [INFO]
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(INFO|ERROR)\]"
    
    results = re.findall(pattern, log_text)
    return results


# 3. 格式化输出：乘法表
def print_multiplication_table():
    print("--- 9x9 Multiplication Table ---")
    for i in range(1, 10):
        row_str = ""
        for j in range(1, i + 1):
            # {j} x {i} = {i*j}
            # :2d 保证结果占2位，对齐
            row_str += f"{j}x{i}={i*j:<2d}  "
        print(row_str)


# 测试代码
if __name__ == "__main__":
    # 测试 1
    print(censor_text("I hate you, HATE!", ["hate"]))
    
    # 测试 2
    log_data = """
    2023-10-01 10:00:01 [INFO] User logged in: user_123
    2023-10-01 10:05:23 [ERROR] Database connection failed
    """
    print("Log entries:", parse_log(log_data))
    
    # 测试 3
    print_multiplication_table()
