# exercise_01_01.py - List Practice
# 请在下方完成练习

# 1. 使用列表推导式生成 1-100 中所有能被 3 或 5 整除的数
divisible_nums = []  # TODO: 用列表推导式实现


# 2. 实现一个函数，将嵌套列表展平
def flatten(nested_list):
    """
    将嵌套列表展平为一维列表
    例如: flatten([[1, 2], [3, 4], [5]]) => [1, 2, 3, 4, 5]
    """
    # TODO: 实现这个函数
    pass


# 3. 使用切片实现回文检查
def is_palindrome(s):
    """
    检查字符串是否是回文
    例如: is_palindrome("racecar") => True
    """
    # TODO: 使用切片实现
    pass


# 测试代码
if __name__ == "__main__":
    # 测试 1
    print("能被 3 或 5 整除的数:", divisible_nums[:10], "...")
    
    # 测试 2
    test_nested = [[1, 2], [3, 4], [5]]
    print("展平结果:", flatten(test_nested))
    
    # 测试 3
    print("racecar 是回文?", is_palindrome("racecar"))
    print("hello 是回文?", is_palindrome("hello"))
