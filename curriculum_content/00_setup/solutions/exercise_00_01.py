import sys
import os
import platform

def check_environment():
    """
    环境自检脚本
    """
    print("="*30)
    print("🛠️  环境自检报告")
    print("="*30)
    
    # 1. Python 版本
    print(f"Python 版本: {sys.version.split()[0]}")
    
    # 2. 操作系统
    print(f"操作系统: {platform.system()} ({platform.release()})")
    
    # 3. 当前工作目录
    print(f"工作目录: {os.getcwd()}")
    
    # 4. 简单的计算验证
    result = 2 ** 10
    print(f"计算测试 (2^10): {result}")
    
    if result == 1024:
        print("\n✅ 计算功能正常")
    else:
        print("\n❌ 计算功能异常")

    print("="*30)
    print("🎉 环境配置完成！")

if __name__ == "__main__":
    check_environment()
