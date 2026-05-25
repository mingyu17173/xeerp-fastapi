# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from common.core.system_env import settings
from common.core.exception import ServiceException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtil:
    @staticmethod
    def encode(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)


class JwtUtil:
    secret = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM
    expire = settings.EXPIRE_HOURS

    @classmethod
    def create_token(cls, payload: dict) -> str:
        expire = datetime.utcnow() + timedelta(hours=cls.expire)
        payload.update({"exp": expire})
        return jwt.encode(payload, cls.secret, algorithm=cls.algorithm)

    @classmethod
    def parse_token(cls, token: str) -> dict:
        try:
            return jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
        except JWTError:
            raise ServiceException("登录已过期，请重新登录", 401)