# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: enums.py
# @Software: PyCharm
# @Desc : 核心配置

from enum import Enum
from typing import Dict, Any


class BusinessType(Enum):
    """
    业务操作类型

    OTHER: 其它
    INSERT: 新增
    UPDATE: 修改
    DELETE: 删除
    GRANT: 授权
    EXPORT: 导出
    IMPORT: 导入
    FORCE: 强退
    GENCODE: 生成代码
    CLEAN: 清空数据
    TRANSFER: 转化
    """

    OTHER = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    GRANT = 4
    EXPORT = 5
    IMPORT = 6
    FORCE = 7
    GENCODE = 8
    CLEAN = 9
    TRANSFER = 10


class RedisInitKeyConfig(Enum):
    """
    系统内置Redis键名
    """

    @property
    def key(self):
        return self.value.get('key')

    @property
    def remark(self):
        return self.value.get('remark')

    ACCESS_TOKEN = {'key': 'access_token', 'remark': '登录令牌信息'}
    SYS_DICT = {'key': 'sys_dict', 'remark': '数据字典'}
    SYS_USER = {'key': 'sys_user', 'remark': '用户信息'}
    SYS_CONFIG = {'key': 'sys_config', 'remark': '配置信息'}
    CAPTCHA_CODES = {'key': 'captcha_codes', 'remark': '图片验证码'}
    ACCOUNT_LOCK = {'key': 'account_lock', 'remark': '用户锁定'}
    PASSWORD_ERROR_COUNT = {'key': 'password_error_count', 'remark': '密码错误次数'}
    SMS_CODE = {'key': 'sms_code', 'remark': '短信验证码'}


class ErrorCode(Enum):
    """
    系统错误码枚举 - 优化版本
    采用模块化分类，便于扩展和维护
    """

    # 认证相关错误码 (1xxx)
    LOGIN_FAILED = "AUTH_1001"
    LOGIN_TIMEOUT = "AUTH_1002"
    LOGIN_LOCKED = "AUTH_1003"
    LOGIN_ATTEMPTS_EXCEEDED = "AUTH_1004"
    USER_NOT_FOUND = "AUTH_1005"
    PASSWORD_INCORRECT = "AUTH_1006"

    # 授权相关错误码 (2xxx)
    AUTH_EXPIRED = "AUTH_2001"
    AUTH_INVALID = "AUTH_2002"
    AUTH_REQUIRED = "AUTH_2003"
    TOKEN_INVALID = "AUTH_2004"
    TOKEN_EXPIRED = "AUTH_2005"

    # 权限相关错误码 (3xxx)
    PERMISSION_DENIED = "PERM_3001"
    ROLE_INSUFFICIENT = "PERM_3002"
    RESOURCE_FORBIDDEN = "PERM_3003"
    OPERATION_NOT_ALLOWED = "PERM_3004"

    # 服务相关错误码 (4xxx)
    SERVICE_ERROR = "SVC_4001"
    SERVICE_UNAVAILABLE = "SVC_4002"
    SERVICE_TIMEOUT = "SVC_4003"
    SERVICE_MAINTENANCE = "SVC_4004"

    # 验证相关错误码 (5xxx)
    VALIDATION_ERROR = "VAL_5001"
    FIELD_REQUIRED = "VAL_5002"
    FIELD_FORMAT_INVALID = "VAL_5003"
    FIELD_LENGTH_EXCEEDED = "VAL_5004"
    DATA_INTEGRITY_ERROR = "VAL_5005"

    # 业务逻辑错误码 (6xxx)
    BUSINESS_RULE_VIOLATION = "BIZ_6001"
    DUPLICATE_ENTRY = "BIZ_6002"
    RESOURCE_NOT_FOUND = "BIZ_6003"
    OPERATION_CONFLICT = "BIZ_6004"

    # 警告类错误码 (7xxx)
    SERVICE_WARNING = "WARN_7001"
    RESOURCE_LOW = "WARN_7002"
    PERFORMANCE_DEGRADED = "WARN_7003"

    # 系统级错误码 (8xxx)
    INTERNAL_ERROR = "SYS_8001"
    DATABASE_ERROR = "SYS_8002"
    EXTERNAL_SERVICE_ERROR = "SYS_8003"


class ErrorCategory(Enum):
    """错误分类枚举"""
    AUTHENTICATION = "AUTH"
    AUTHORIZATION = "AUTHZ"
    PERMISSION = "PERM"
    SERVICE = "SVC"
    VALIDATION = "VAL"
    BUSINESS = "BIZ"
    WARNING = "WARN"
    SYSTEM = "SYS"


class ErrorCodeManager:
    """错误码管理器"""

    # 错误码描述映射
    ERROR_DESCRIPTIONS: Dict[ErrorCode, str] = {
        ErrorCode.LOGIN_FAILED: "登录失败，用户名或密码错误",
        ErrorCode.LOGIN_TIMEOUT: "登录会话已超时",
        ErrorCode.LOGIN_LOCKED: "账户已被锁定，请联系管理员",
        ErrorCode.LOGIN_ATTEMPTS_EXCEEDED: "登录尝试次数过多，请稍后重试",
        ErrorCode.USER_NOT_FOUND: "用户不存在",
        ErrorCode.PASSWORD_INCORRECT: "密码不正确",
        ErrorCode.AUTH_EXPIRED: "认证已过期，请重新登录",
        ErrorCode.AUTH_INVALID: "无效的认证信息",
        ErrorCode.AUTH_REQUIRED: "需要认证才能访问此资源",
        ErrorCode.TOKEN_INVALID: "令牌无效",
        ErrorCode.TOKEN_EXPIRED: "令牌已过期",
        ErrorCode.PERMISSION_DENIED: "权限不足，无法访问此资源",
        ErrorCode.ROLE_INSUFFICIENT: "角色权限不足",
        ErrorCode.RESOURCE_FORBIDDEN: "资源访问被禁止",
        ErrorCode.OPERATION_NOT_ALLOWED: "当前操作不被允许",
        ErrorCode.SERVICE_ERROR: "服务内部错误",
        ErrorCode.SERVICE_UNAVAILABLE: "服务暂时不可用",
        ErrorCode.SERVICE_TIMEOUT: "服务请求超时",
        ErrorCode.SERVICE_MAINTENANCE: "系统维护中，请稍后访问",
        ErrorCode.VALIDATION_ERROR: "数据验证失败",
        ErrorCode.FIELD_REQUIRED: "必填字段不能为空",
        ErrorCode.FIELD_FORMAT_INVALID: "字段格式不正确",
        ErrorCode.FIELD_LENGTH_EXCEEDED: "字段长度超过限制",
        ErrorCode.DATA_INTEGRITY_ERROR: "数据完整性错误",
        ErrorCode.BUSINESS_RULE_VIOLATION: "违反业务规则",
        ErrorCode.DUPLICATE_ENTRY: "重复的数据条目",
        ErrorCode.RESOURCE_NOT_FOUND: "请求的资源不存在",
        ErrorCode.OPERATION_CONFLICT: "操作冲突",
        ErrorCode.SERVICE_WARNING: "服务警告",
        ErrorCode.RESOURCE_LOW: "资源不足警告",
        ErrorCode.PERFORMANCE_DEGRADED: "性能下降警告",
        ErrorCode.INTERNAL_ERROR: "系统内部错误",
        ErrorCode.DATABASE_ERROR: "数据库操作错误",
        ErrorCode.EXTERNAL_SERVICE_ERROR: "外部服务调用错误",
    }

    # 错误码HTTP状态码映射
    ERROR_HTTP_STATUS: Dict[ErrorCode, int] = {
        ErrorCode.LOGIN_FAILED: 401,
        ErrorCode.LOGIN_TIMEOUT: 401,
        ErrorCode.LOGIN_LOCKED: 423,
        ErrorCode.LOGIN_ATTEMPTS_EXCEEDED: 429,
        ErrorCode.USER_NOT_FOUND: 404,
        ErrorCode.PASSWORD_INCORRECT: 401,
        ErrorCode.AUTH_EXPIRED: 401,
        ErrorCode.AUTH_INVALID: 401,
        ErrorCode.AUTH_REQUIRED: 401,
        ErrorCode.TOKEN_INVALID: 401,
        ErrorCode.TOKEN_EXPIRED: 401,
        ErrorCode.PERMISSION_DENIED: 403,
        ErrorCode.ROLE_INSUFFICIENT: 403,
        ErrorCode.RESOURCE_FORBIDDEN: 403,
        ErrorCode.OPERATION_NOT_ALLOWED: 403,
        ErrorCode.SERVICE_ERROR: 500,
        ErrorCode.SERVICE_UNAVAILABLE: 503,
        ErrorCode.SERVICE_TIMEOUT: 504,
        ErrorCode.SERVICE_MAINTENANCE: 503,
        ErrorCode.VALIDATION_ERROR: 422,
        ErrorCode.FIELD_REQUIRED: 422,
        ErrorCode.FIELD_FORMAT_INVALID: 422,
        ErrorCode.FIELD_LENGTH_EXCEEDED: 422,
        ErrorCode.DATA_INTEGRITY_ERROR: 422,
        ErrorCode.BUSINESS_RULE_VIOLATION: 400,
        ErrorCode.DUPLICATE_ENTRY: 409,
        ErrorCode.RESOURCE_NOT_FOUND: 404,
        ErrorCode.OPERATION_CONFLICT: 409,
        ErrorCode.SERVICE_WARNING: 200,
        ErrorCode.RESOURCE_LOW: 200,
        ErrorCode.PERFORMANCE_DEGRADED: 200,
        ErrorCode.INTERNAL_ERROR: 500,
        ErrorCode.DATABASE_ERROR: 500,
        ErrorCode.EXTERNAL_SERVICE_ERROR: 502,
    }

    @classmethod
    def get_description(cls, error_code: ErrorCode) -> str:
        """获取错误码描述"""
        return cls.ERROR_DESCRIPTIONS.get(error_code, "未知错误")

    @classmethod
    def get_http_status(cls, error_code: ErrorCode) -> int:
        """获取错误码对应的HTTP状态码"""
        return cls.ERROR_HTTP_STATUS.get(error_code, 400)

    @classmethod
    def get_category(cls, error_code: ErrorCode) -> ErrorCategory:
        """获取错误码所属分类"""
        code_prefix = error_code.value.split('_')[0]
        for category in ErrorCategory:
            if category.value == code_prefix:
                return category
        return ErrorCategory.SYSTEM

    @classmethod
    def get_error_info(cls, error_code: ErrorCode) -> Dict[str, Any]:
        """获取完整的错误信息"""
        return {
            "error_code": error_code.value,
            "message": cls.get_description(error_code),
            "http_status": cls.get_http_status(error_code),
            "category": cls.get_category(error_code).value,
            "description": cls.get_description(error_code)
        }
