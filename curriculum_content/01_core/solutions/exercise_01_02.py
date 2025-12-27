# exercise_01_02.py - Reference Solution
# 参考答案

from collections import Counter

# 1. 词频统计加强版
def top_3_words(text):
    """
    统计每个单词出现的次数，并找出出现频率最高的前 3 个单词。
    """
    # 简单的预处理：转小写，移除标点（这里简化处理，只移除逗号和句号）
    clean_text = text.lower().replace(',', '').replace('.', '')
    words = clean_text.split()
    
    # 使用 Counter 统计
    counter = Counter(words)
    
    # 获取前 3 个
    return counter.most_common(3)


# 2. 集合运算实战
def analyze_classes(class_a, class_b):
    set_a = set(class_a)
    set_b = set(class_b)
    
    both = set_a & set_b
    only_a = set_a - set_b
    all_students = set_a | set_b
    
    return both, only_a, all_students


# 3. 字典转换
def list_to_dict(tuple_list):
    """
    将 [("key", "value"), ...] 转换为字典
    """
    return dict(tuple_list)


# 测试代码
if __name__ == "__main__":
    # 测试 1
    sample_text = "Python is great. Python is simple. Python is powerful. Coding is fun."
    print("Top 3 words:", top_3_words(sample_text))
    
    # 测试 2
    class_a = ["Alice", "Bob", "Charlie", "David"]
    class_b = ["Charlie", "David", "Eve", "Frank"]
    both, only_a, all_std = analyze_classes(class_a, class_b)
    print("两个班都有:", both)
    print("只在 A 班:", only_a)
    print("所有学生:", all_std)
    
    # 测试 3
    data_list = [("name", "Alice"), ("age", 30), ("city", "New York")]
    print("转换后的字典:", list_to_dict(data_list))
