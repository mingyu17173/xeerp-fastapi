# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: pwd_util.py
# @Software: PyCharm
# @Desc : 工具类

from passlib.context import CryptContext
from typing import Optional

# 配置密码加密上下文（bcrypt 是目前最安全、最通用的哈希算法）
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # 安全强度：12 是企业标准
)

class PwdUtil:
    """
    企业级密码工具类
    功能：密码加密 / 密码校验 / 自动长度限制 / 安全防护
    """

    @classmethod
    def verify_password(
        cls,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        """
        校验明文密码与哈希密码是否匹配
        :param plain_password: 明文密码
        :param hash_password: 数据库存储的哈希密码
        :return: bool
        """
        if not plain_password or not hashed_password:
            return False

        # bcrypt 限制最大 72 字节，自动截断，防止报错
        plain_password = plain_password.encode("utf-8")[:72].decode("utf-8", "ignore")

        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    @classmethod
    def get_password_hash(
        cls,
        input_password: str,
        salt: Optional[str] = None
    ) -> str:
        """
        明文密码 → 安全哈希加密
        :param input_password: 明文密码
        :return: 哈希密码字符串
        """
        if not input_password:
            raise ValueError("密码不能为空")

        # bcrypt 最大支持 72 字节，自动截断
        input_password = input_password.encode("utf-8")[:72].decode("utf-8", "ignore")

        return pwd_context.hash(input_password)