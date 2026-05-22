"""
Gateway Service Authentication
网关服务认证模块
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, Request
from core.env import AppConfig

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT Token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=AppConfig.jwt_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": "xeerp-gateway"
    })
    
    encoded_jwt = jwt.encode(to_encode, AppConfig.jwt_secret_key, algorithm=AppConfig.jwt_algorithm)
    return encoded_jwt


def verify_jwt_token(token: str) -> Dict:
    """
    验证 JWT Token
    """
    try:
        payload = jwt.decode(
            token, 
            AppConfig.jwt_secret_key, 
            algorithms=[AppConfig.jwt_algorithm],
            options={"verify_exp": True, "verify_iss": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="无效的签发者")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的 Token")


async def get_current_user(request: Request) -> Dict:
    """
    获取当前用户信息
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="未授权访问")
    
    return verify_jwt_token(token)


class AuthError(Exception):
    """认证错误异常"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail