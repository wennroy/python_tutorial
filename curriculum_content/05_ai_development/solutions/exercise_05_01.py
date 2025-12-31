"""
练习 05-01: 创建一个代码解释器

使用 LangChain 构建一个能解释 Python 代码的 AI 工具
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class CodeExplanation(BaseModel):
    """代码解释结果"""
    summary: str = Field(description="一句话概括代码功能")
    detailed_explanation: str = Field(description="详细的代码解释，逐行或逐块说明")
    potential_issues: list[str] = Field(description="潜在的问题或 Bug")
    improvements: list[str] = Field(description="改进建议")
    complexity: str = Field(description="时间/空间复杂度分析（如适用）")


def create_code_explainer():
    """创建代码解释器"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    parser = PydanticOutputParser(pydantic_object=CodeExplanation)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个资深的 Python 代码审查专家。
请详细分析用户提供的代码，从以下几个维度进行解释：

1. 功能概述：用一句话说明代码做什么
2. 详细解释：逐行或逐块解释代码逻辑
3. 潜在问题：指出可能的 Bug、安全问题或性能问题
4. 改进建议：提供具体可行的改进方案
5. 复杂度分析：如果涉及算法，分析时间/空间复杂度

{format_instructions}"""),
        ("human", "请分析以下 Python 代码：\n\n```python\n{code}\n```")
    ])
    
    # 注入格式说明
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    
    # 构建链
    chain = prompt | llm | parser
    
    return chain


def explain_code(code: str) -> CodeExplanation:
    """解释代码"""
    explainer = create_code_explainer()
    return explainer.invoke({"code": code})


def main():
    # 测试代码示例
    test_code = '''
def find_duplicates(lst):
    seen = []
    duplicates = []
    for item in lst:
        if item in seen:
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.append(item)
    return duplicates

# 使用示例
numbers = [1, 2, 3, 2, 4, 3, 5]
print(find_duplicates(numbers))
'''
    
    print("=" * 60)
    print("代码解释器")
    print("=" * 60)
    print("\n【待分析的代码】")
    print(test_code)
    print("\n【分析结果】")
    print("-" * 60)
    
    result = explain_code(test_code)
    
    print(f"\n📋 功能概述:\n   {result.summary}")
    print(f"\n📖 详细解释:\n{result.detailed_explanation}")
    print(f"\n⚠️ 潜在问题:")
    for issue in result.potential_issues:
        print(f"   • {issue}")
    print(f"\n💡 改进建议:")
    for improvement in result.improvements:
        print(f"   • {improvement}")
    print(f"\n📊 复杂度分析:\n   {result.complexity}")


if __name__ == "__main__":
    main()
