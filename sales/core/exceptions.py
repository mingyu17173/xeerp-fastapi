"""
Sales Service Custom Exceptions
销售服务自定义异常
"""

class SalesException(Exception):
    """销售服务基础异常"""
    def __init__(self, message: str = "销售服务异常"):
        super().__init__(message)
        self.message = message

class OrderNotFoundError(SalesException):
    """订单不存在"""
    def __init__(self):
        super().__init__("订单不存在")

class OrderCodeExistsError(SalesException):
    """订单编号已存在"""
    def __init__(self):
        super().__init__("订单编号已存在")

class OrderStatusError(SalesException):
    """订单状态错误"""
    def __init__(self, message: str = "订单状态错误"):
        super().__init__(message)

class InsufficientStockError(SalesException):
    """库存不足"""
    def __init__(self):
        super().__init__("库存不足")

class CustomerNotFoundError(SalesException):
    """客户不存在"""
    def __init__(self):
        super().__init__("客户不存在")

class ProductNotFoundError(SalesException):
    """商品不存在"""
    def __init__(self):
        super().__init__("商品不存在")