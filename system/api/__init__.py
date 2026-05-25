# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

from fastapi import APIRouter, FastAPI

# 系统基础配置(system)
from .v1.cache_controller import cacheRoute
from .v1.captcha_controller import captchaRoute
from .v1.common_controller import commonRoute
from .v1.config_controller import configRoute
from .v1.dept_controller import deptRoute
from .v1.dict_controller import dictRoute
from .v1.log_controller import logRoute
from .v1.login_controller import loginRoute
from .v1.job_controller import jobRoute
from .v1.menu_controller import menuRoute
from .v1.notice_controller import noticeRoute
from .v1.online_controller import onlineRoute
from .v1.post_controler import postRoute
from .v1.role_controller import roleRoute
from .v1.server_controller import serverRoute
from .v1.user_controller import userRoute
from .v1.region_controller import regionRoute

# from .gen.gen_controller import genRoute


v1 = APIRouter()

# 系统基础配置(system)
v1.include_router(loginRoute, tags=["登录模块"])
v1.include_router(captchaRoute, tags=["验证码模块"])
v1.include_router(userRoute, tags=["系统管理-用户管理"])
v1.include_router(roleRoute, tags=["系统管理-角色管理"])
v1.include_router(menuRoute, tags=["系统管理-菜单管理"])
v1.include_router(deptRoute, tags=["系统管理-部门管理"])
v1.include_router(postRoute, tags=["系统管理-部门管理"])
v1.include_router(dictRoute, tags=["系统管理-字典管理"])
v1.include_router(configRoute, tags=["系统管理-参数管理"])
v1.include_router(noticeRoute, tags=["系统管理-通知公告管理"])
v1.include_router(logRoute, tags=["系统管理-日志管理"])
v1.include_router(onlineRoute, tags=["系统管理-在线用户"])
v1.include_router(jobRoute, tags=["系统监控-定时任务"])
v1.include_router(serverRoute, tags=["系统监控-菜单管理"])
v1.include_router(cacheRoute, tags=["系统监控-缓存监控"])
v1.include_router(commonRoute, tags=["通用模块"])
v1.include_router(regionRoute, tags=["地区管理"])


# 注册路由
def register_routers(app: FastAPI):

    app.include_router(v1)