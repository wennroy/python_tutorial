# exercise_extra_03.py - Reference Solution
# 参考答案

import logging
import sys

def setup_logger():
    # 1. 创建 Logger
    logger = logging.getLogger("ecommerce")
    logger.setLevel(logging.INFO) # 总开关设为 INFO，否则 DEBUG 级别的 FileHandler 也没用
    
    # 防止重复添加 Handler (如果在 Notebook 或多次调用中)
    if logger.handlers:
        return logger

    # 2. 创建 Formatter
    # 包含：时间戳、日志级别、文件名、行号、消息
    # %(filename)s: 文件名
    # %(lineno)d: 行号
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
    )

    # 3. 创建 Handlers
    
    # 控制台 Handler: WARNING 及以上
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # 文件 Handler: INFO 及以上
    file_handler = logging.FileHandler("orders.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # 4. 添加 Handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def simulate_ecommerce():
    logger = setup_logger()
    
    print("--- Simulation Start ---")
    
    # 场景 1: 正常下单 (INFO)
    # 应该只出现在 orders.log，不出现在控制台
    logger.info("用户 'Alice' 下单成功，订单号 #1001")
    
    # 场景 2: 库存警告 (WARNING)
    # 应该同时出现在 orders.log 和控制台
    logger.warning("库存不足，商品 ID 888 仅剩 2 件")
    
    # 场景 3: 支付错误 (ERROR)
    # 应该同时出现在 orders.log 和控制台
    logger.error("支付网关超时，订单 #1002 支付失败")
    
    # 场景 4: 调试信息 (DEBUG)
    # 应该都不出现，因为总开关是 INFO
    logger.debug("正在计算运费...")
    
    print("--- Simulation End ---")
    print("Check 'orders.log' for full details.")

if __name__ == "__main__":
    simulate_ecommerce()
