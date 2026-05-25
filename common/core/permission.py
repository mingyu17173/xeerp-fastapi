# -*- coding: utf-8 -*-
from functools import wraps
from fastapi import Request, Depends
from common.schemas.common_schema import LoginUserInfo
from common.core.exception import ServiceException
from common.core.security import JwtUtil

# -------------------------
# 从请求头获取当前用户
# -------------------------
async def get_current_user(request: Request) -> LoginUserInfo:
    token = request.headers.get("Authorization", "")
    if not token:
        raise ServiceException("请先登录", 401)
    if token.startswith("Bearer "):
        token = token[7:]

    payload = JwtUtil.parse_token(token)
    return LoginUserInfo(**payload)


# -------------------------
# 功能权限装饰器
# -------------------------
def CheckPerm(perm: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            user: LoginUserInfo = kwargs.get("user")

            if not user:
                raise ServiceException("请先登录", 401)

            # 超级管理员
            if "*" in user.perms:
                return await func(*args, **kwargs)

            if perm not in user.perms:
                raise ServiceException(f"无权限：{perm}", 403)

            return await func(*args, **kwargs)
        return wrapper
    return decorator


# -------------------------
# 数据权限构造器
# -------------------------
class DataPermission:
    @staticmethod
    def get_filter(model, user: LoginUserInfo):
        scope = user.data_scope

        # 1全部 2本部门及子级 3本部门 4本人 5自定义部门
        if scope == 1:
            return True
        if scope == 4:
            return model.create_user_id == user.user_id
        if scope == 3:
            return model.create_dept_id == user.dept_id
        if scope == 5:
            return model.create_dept_id.in_(user.custom_dept_ids or [])

        # 默认本部门
        return model.create_dept_id == user.dept_id