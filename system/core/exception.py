from typing import Optional, Dict, Any
from core.enums import ErrorCode

class BaseException(Exception):
    """
    自定义基础异常BaseException
    """

    def __init__(self, error_code: ErrorCode, message: str = None, data: Optional[Dict[str, Any]] = None, http_status: int = 400, details: Optional[str] = None):
        self.error_code = error_code
        self.message = message
        self.data = data
        self.http_status = http_status
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """
        将异常信息转换为字典格式
        """
        return {
            "error_code": self.error_code.value,
            "message": self.message,
            "data": self.data,
            "http_status": self.http_status,
            "details": self.details,
            "exception_type": self.__class__.__name__,
        }

    def __str__(self) -> str:
        """
        将异常信息转换为字符串格式
        """

        return f"[{self.error_code.value}] {self.message}"


class LoginException(BaseException):
    """
    自定义登录异常LoginException
    """

    def __init__(self, message: str = "登录失败", data: Optional[Dict[str, Any]] = None,  details: Optional[str] = None ):
        super().__init__(error_code=ErrorCode.LOGIN_FAILED, message=message, data=data, http_status=401, details=details)


class AuthException(BaseException):
    """
    自定义令牌异常AuthException
    """

    def __init__(self, message: str = "令牌验证失败", data: Optional[Dict[str, Any]] = None, details: Optional[str] = None):
        super().__init__(error_code=ErrorCode.AUTH_EXPIRED, message=message, data=data, http_status=403, details=details)


class PermissionException(BaseException):
    """
    自定义权限异常PermissionException
    """

    def __init__(self, message: str = "权限不足", data: Optional[Dict[str, Any]] = None, details: Optional[str] = None):
        super().__init__(error_code=ErrorCode.PERMISSION_DENIED, message=message, data=data, http_status=403, details=details)


class ServiceException(BaseException):
    """
    自定义服务异常ServiceException
    """

    def __init__(self, message: str = "服务异常", data: Optional[Dict[str, Any]] = None, details: Optional[str] = None):
        super().__init__(error_code=ErrorCode.SERVICE_ERROR, message=message, data=data, http_status=500, details=details)


class ServiceWarning(BaseException):
    """
    自定义服务警告ServiceWarning
    """

    def __init__(self, message: str = "服务警告", data: Optional[Dict[str, Any]] = None, details: Optional[str] = None):
        super().__init__(error_code=ErrorCode.SERVICE_WARNING, message=message, data=data, http_status=200, details=details)


class ModelValidatorException(BaseException):
    """
    自定义模型校验异常ModelValidatorException
    """

    def __init__(self, message: str = "模型校验失败", data: Optional[Dict[str, Any]] = None, details: Optional[str] = None):
        super().__init__(error_code=ErrorCode.VALIDATION_ERROR, message=message, data=data, http_status=422, details=details)
