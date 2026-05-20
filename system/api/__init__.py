from fastapi import APIRouter, FastAPI

# 系统基础配置(system)
from api.v1.cache_controller import cacheController
from api.v1.captcha_controller import captchaController
from api.v1.common_controller import commonController
from api.v1.config_controller import configController
from api.v1.dept_controller import deptController
from api.v1.dict_controller import dictController
from api.v1.log_controller import logController
from api.v1.login_controller import loginController
from api.v1.job_controller import jobController
from api.v1.menu_controller import menuController
from api.v1.notice_controller import noticeController
from api.v1.online_controller import onlineController
from api.v1.post_controler import postController
from api.v1.role_controller import roleController
from api.v1.server_controller import serverController
from api.v1.user_controller import userController
from api.v1.region_controller import regionController

# from api.gen.gen_controller import genController

v1 = APIRouter()

# 系统基础配置(system)
v1.include_router(loginController, tags=["登录模块"])
v1.include_router(captchaController, tags=["验证码模块"])
v1.include_router(userController, tags=["系统管理-用户管理"])
v1.include_router(roleController, tags=["系统管理-角色管理"])
v1.include_router(menuController, tags=["系统管理-菜单管理"])
v1.include_router(deptController, tags=["系统管理-部门管理"])
v1.include_router(postController, tags=["系统管理-部门管理"])
v1.include_router(dictController, tags=["系统管理-字典管理"])
v1.include_router(configController, tags=["系统管理-参数管理"])
v1.include_router(noticeController, tags=["系统管理-通知公告管理"])
v1.include_router(logController, tags=["系统管理-日志管理"])
v1.include_router(onlineController, tags=["系统管理-在线用户"])
v1.include_router(jobController, tags=["系统监控-定时任务"])
v1.include_router(serverController, tags=["系统监控-菜单管理"])
v1.include_router(cacheController, tags=["系统监控-缓存监控"])
v1.include_router(commonController, tags=["通用模块"])
v1.include_router(regionController, tags=["地区管理"])


# 注册路由
def register_routers(app: FastAPI):

    app.include_router(v1)