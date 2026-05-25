# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: auth.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Gateway Service Authentication
网关服务认证模块
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, Request
from core.env import AppConfig
from core.get_redis import RedisUtil


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
        "iss": "xeerp-system"
    })
    
    encoded_jwt = jwt.encode(to_encode, AppConfig.jwt_secret_key, algorithm=AppConfig.jwt_algorithm)
    return encoded_jwt


def verify_jwt_token(token: str) -> Dict:
    """
    验证 JWT Token
    注意：不验证iss字段，因为system服务生成的token没有设置iss
    """
    try:
        payload = jwt.decode(
            token, 
            AppConfig.jwt_secret_key, 
            algorithms=[AppConfig.jwt_algorithm],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的 Token")


async def verify_jwt_token_with_redis(token: str, redis) -> Dict:
    """
    验证 JWT Token 并检查Redis中的有效性
    
    Args:
        token: JWT Token字符串
        redis: Redis连接对象
        
    Returns:
        Token payload
        
    Raises:
        HTTPException: Token验证失败
    """
    # 先验证JWT签名和过期时间
    payload = verify_jwt_token(token)
    
    # 从payload获取session_id或user_id
    session_id = payload.get('session_id')
    user_id = payload.get('user_id')
    
    if not session_id and not user_id:
        raise HTTPException(status_code=401, detail="Token中缺少用户标识")
    
    # 检查Redis中是否存在该Token
    redis_key = f"ACCESS_TOKEN:{session_id}" if session_id else f"ACCESS_TOKEN:{user_id}"
    redis_token = await RedisUtil.get_token_from_redis(redis, redis_key)
    
    if not redis_token:
        raise HTTPException(status_code=401, detail="Token已失效，请重新登录")
    
    if redis_token != token:
        raise HTTPException(status_code=401, detail="Token不匹配，请重新登录")
    
    return payload


async def get_current_user(request: Request) -> Dict:
    """
    获取当前用户信息（带Redis验证）
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="未授权访问")
    
    # 获取Redis连接
    redis = getattr(request.app.state, 'redis', None)
    if not redis:
        raise HTTPException(status_code=500, detail="Redis连接不可用")
    
    # 验证Token（JWT + Redis）
    return await verify_jwt_token_with_redis(token, redis)


class AuthError(Exception):
    """认证错误异常"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail