from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException
from core.env import AppConfig


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT Token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=AppConfig.jwt_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AppConfig.jwt_secret_key, algorithm=AppConfig.jwt_algorithm)
    return encoded_jwt


def verify_jwt_token(token: str) -> dict:
    """
    验证 JWT Token
    """
    try:
        payload = jwt.decode(token, AppConfig.jwt_secret_key, algorithms=[AppConfig.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的 Token")


class JWTBearer:
    """
    JWT 认证依赖
    """
    def __call__(self, token: str):
        return verify_jwt_token(token)