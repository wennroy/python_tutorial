# 模块 4-5 练习参考答案: 常用设计模式实战

import time
from abc import ABC, abstractmethod

# --- 1. 装饰器模式 (Decorator) ---
def log_execution_time(func):
    def wrapper(*args, **kwargs):
        print(f"--- 开始处理: {func.__name__} ---")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"--- 完成处理: {func.__name__}, 耗时: {end_time - start_time:.4f}s ---")
        return result
    return wrapper

# --- 2. 策略模式 (Strategy) ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"💳 信用卡支付成功: ${amount}")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"🅿️ PayPal 支付成功: ${amount}")

# --- 3. 管道模式 (Pipeline) ---
class OrderPipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, func):
        self.stages.append(func)
        return self

    @log_execution_time # 使用装饰器记录整个管道的执行时间
    def process(self, order):
        print(f"初始订单: {order}")
        for stage in self.stages:
            order = stage(order)
            if order is None:
                print("管道处理中断！")
                return None
        return order

# --- 管道阶段函数 ---
def validate_stock(order):
    print("Checking stock...")
    # 模拟库存检查
    if order["qty"] > 10:
        print("Error: 库存不足！")
        return None
    return order

def calculate_discount(order):
    print("Calculating discount...")
    if order["qty"] >= 2:
        order["discount"] = 0.1 # 10% off
    else:
        order["discount"] = 0
    
    order["final_price"] = order["price"] * order["qty"] * (1 - order["discount"])
    return order

def generate_invoice(order):
    print("Generating invoice...")
    order["invoice_id"] = f"INV-{int(time.time())}"
    return order

# --- 主程序 ---
if __name__ == "__main__":
    # 1. 准备订单
    my_order = {"item": "Python Book", "price": 50, "qty": 2}

    # 2. 构建管道
    pipeline = OrderPipeline()
    pipeline.add_stage(validate_stock)\
            .add_stage(calculate_discount)\
            .add_stage(generate_invoice)

    # 3. 执行管道
    processed_order = pipeline.process(my_order)

    # 4. 支付 (策略模式)
    if processed_order:
        print(f"\n最终订单详情: {processed_order}")
        
        # 选择支付策略
        payment_method = CreditCardPayment() # 可以随时换成 PayPalPayment()
        payment_method.pay(processed_order["final_price"])
