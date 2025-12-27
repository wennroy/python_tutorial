# exercise_02_03.py - Text Analyzer
# 练习 02-03: AI 辅助调试

def analyze_text(text):
    """
    统计文本中的单词数量和平均单词长度
    """
    if not text:
        return {"word_count": 0, "avg_length": 0}
        
    # Bug 1: split() 默认按空格分割，但如果有标点符号粘连怎么办？
    # 例如 "hello, world" -> ["hello,", "world"] -> "hello," 长度是 6
    words = text.split()
    
    total_length = 0
    for word in words:
        total_length += len(word)
        
    # Bug 2: 如果 text 全是空格，words 为空，这里会除以零
    # 例如 text = "   "
    avg_length = total_length / len(words)
    
    return {
        "word_count": len(words),
        "avg_length": avg_length
    }

def get_summary(stats):
    # Bug 3: 拼写错误 'avg_len' vs 'avg_length'
    return f"Found {stats['word_count']} words, average length: {stats['avg_len']:.2f}"

if __name__ == "__main__":
    # 测试用例 1: 正常文本
    sample1 = "Python is amazing"
    print(f"Analyzing '{sample1}'...")
    stats1 = analyze_text(sample1)
    print(get_summary(stats1)) # 这里会报错 (KeyError)
    
    # 任务：使用 Copilot 解释 KeyError 并修复 get_summary 函数
    
    # 测试用例 2: 空格文本
    sample2 = "   "
    print(f"\nAnalyzing '{sample2}'...")
    # stats2 = analyze_text(sample2) # 这里会报错 (ZeroDivisionError)
    # print(stats2)
    
    # 任务：使用 Copilot 修复 analyze_text 中的除零错误
    
    # 测试用例 3: 标点符号
    sample3 = "Hello, world!"
    print(f"\nAnalyzing '{sample3}'...")
    stats3 = analyze_text(sample3)
    print(f"Stats: {stats3}") 
    # 观察结果：'Hello,' 长度被算作 6，'world!' 被算作 6。
    # 任务：询问 Copilot "如何让 split 忽略标点符号？" 并优化代码。
