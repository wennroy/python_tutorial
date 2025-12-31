"""
练习 05-02: 多语言翻译器 + 面试题生成器

演示 LangChain 的并行处理和结构化输出
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# Part 1: 多语言翻译器
# ============================================================

class MultilingualTranslator:
    """多语言并行翻译器"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.parser = StrOutputParser()
        
        # 为每种语言创建翻译链
        self.translate_prompt = ChatPromptTemplate.from_template(
            "将以下文本翻译成{language}，只输出翻译结果：\n\n{text}"
        )
    
    def create_translation_chain(self, language: str):
        """创建单语言翻译链"""
        return (
            self.translate_prompt.partial(language=language) 
            | self.llm 
            | self.parser
        )
    
    def translate(self, text: str, languages: list[str] = None) -> dict:
        """并行翻译到多种语言"""
        if languages is None:
            languages = ["中文", "日语", "法语", "西班牙语"]
        
        # 构建并行链
        parallel_chains = {
            lang: self.create_translation_chain(lang)
            for lang in languages
        }
        
        parallel_runner = RunnableParallel(**parallel_chains)
        
        # 执行并行翻译
        results = parallel_runner.invoke({"text": text})
        
        return results


def demo_translator():
    """演示翻译器"""
    print("=" * 60)
    print("多语言翻译器")
    print("=" * 60)
    
    translator = MultilingualTranslator()
    
    original_text = "Artificial Intelligence is transforming how we work and live."
    
    print(f"\n📝 原文:\n   {original_text}\n")
    print("🌐 翻译中...")
    
    translations = translator.translate(original_text)
    
    print("\n📋 翻译结果:")
    for lang, result in translations.items():
        print(f"   [{lang}] {result}")


# ============================================================
# Part 2: 面试题生成器
# ============================================================

class InterviewQuestion(BaseModel):
    """单个面试题"""
    question: str = Field(description="面试问题")
    key_points: list[str] = Field(description="考察要点，3-5 个")
    sample_answer: str = Field(description="参考答案")
    follow_up: str = Field(description="可能的追问")


class InterviewQuestionSet(BaseModel):
    """面试题集合"""
    position: str = Field(description="目标职位")
    difficulty: str = Field(description="难度级别")
    questions: list[InterviewQuestion] = Field(description="面试题列表，3 道题")


class InterviewQuestionGenerator:
    """面试题生成器"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.parser = PydanticOutputParser(pydantic_object=InterviewQuestionSet)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个资深的技术面试官。
请根据用户指定的职位和难度，生成高质量的面试题。

每道题目需要包含：
1. 问题本身
2. 考察要点（评判标准）
3. 参考答案
4. 可能的追问

{format_instructions}"""),
            ("human", "请为 {position} 职位生成 3 道 {difficulty} 难度的面试题")
        ])
        
        self.prompt = self.prompt.partial(
            format_instructions=self.parser.get_format_instructions()
        )
        
        self.chain = self.prompt | self.llm | self.parser
    
    def generate(self, position: str, difficulty: str) -> InterviewQuestionSet:
        """生成面试题"""
        return self.chain.invoke({
            "position": position,
            "difficulty": difficulty
        })


def demo_interview_generator():
    """演示面试题生成器"""
    print("\n" + "=" * 60)
    print("面试题生成器")
    print("=" * 60)
    
    generator = InterviewQuestionGenerator()
    
    position = "Python 后端工程师"
    difficulty = "中等"
    
    print(f"\n🎯 职位: {position}")
    print(f"📊 难度: {difficulty}")
    print("\n⏳ 生成中...")
    
    result = generator.generate(position, difficulty)
    
    print(f"\n📋 生成了 {len(result.questions)} 道面试题:\n")
    
    for i, q in enumerate(result.questions, 1):
        print(f"{'─' * 50}")
        print(f"问题 {i}: {q.question}")
        print(f"\n考察要点:")
        for point in q.key_points:
            print(f"   • {point}")
        print(f"\n参考答案:\n   {q.sample_answer}")
        print(f"\n追问: {q.follow_up}")
        print()


def main():
    # 运行翻译器演示
    demo_translator()
    
    # 运行面试题生成器演示
    demo_interview_generator()


if __name__ == "__main__":
    main()
