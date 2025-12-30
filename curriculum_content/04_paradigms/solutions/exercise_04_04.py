# 模块 4-3 练习参考答案: OOP 重构为 FP

import re

# 原始 OOP 代码 (为了对比保留在此)
class TextProcessor:
    def __init__(self, text):
        self.text = text

    def clean(self):
        self.text = self.text.strip().lower()

    def remove_special_chars(self):
        self.text = re.sub(r'[^a-z0-9\s]', '', self.text)

    def get_words(self):
        return self.text.split()

# --- 重构后的 FP 代码 ---

def clean_text(text: str) -> str:
    """去除首尾空格并转小写"""
    return text.strip().lower()

def remove_special_chars(text: str) -> str:
    """移除特殊字符"""
    return re.sub(r'[^a-z0-9\s]', '', text)

def get_words(text: str) -> list[str]:
    """分割为单词列表"""
    return text.split()

def process_pipeline(text: str) -> list[str]:
    """组合函数形成流水线"""
    # 数据流向: text -> clean -> remove_special -> split
    step1 = clean_text(text)
    step2 = remove_special_chars(step1)
    return get_words(step2)

# 测试验证
if __name__ == "__main__":
    raw_text = "  Hello, World! 123  "
    
    # OOP 运行
    processor = TextProcessor(raw_text)
    processor.clean()
    processor.remove_special_chars()
    oop_result = processor.get_words()
    print(f"OOP Result: {oop_result}")

    # FP 运行
    fp_result = process_pipeline(raw_text)
    print(f"FP Result:  {fp_result}")

    assert oop_result == fp_result, "两种实现结果不一致！"
    print("测试通过！")
