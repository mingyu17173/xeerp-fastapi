# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: whitelist.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Gateway Whitelist Configuration
网关白名单配置模块

用于管理免鉴权访问的接口路径，支持：
1. 精确匹配路径（Exact Match）
2. 前缀匹配路径（Prefix Match）
3. 正则匹配路径（Regex Match）
4. 方法级路径配置（Method + Path）
"""

from typing import Set, Dict, Pattern
import re


class WhitelistConfig:
    """
    白名单配置类
    """
    
    # ==================== 精确匹配路径 ====================
    # 完全匹配的免鉴权路径
    EXACT_PATHS: Set[str] = {
        # 文档接口
        "/api/docs",
        "/api/redoc",
        "/api/openapi.json",
        
        # 健康检查
        "/health",
        "/healthz",
        
        # 首页
        "/",
    }
    
    # ==================== 前缀匹配路径 ====================
    # 前缀匹配的免鉴权路径（以这些前缀开头的路径都免鉴权）
    PREFIX_PATHS: Set[str] = {
        # 认证相关
        "/api/auth/",           # 登录、登出等认证接口
        "/api/login/",          # 登录相关接口
        "/api/logout/",         # 登出相关接口
        
        # 验证码
        "/api/captcha/",        # 验证码相关接口
        
        # 公共数据
        "/api/public/",         # 公共数据接口
        "/api/common/",         # 通用接口
        
        # 静态资源
        "/static/",             # 静态资源
        "/favicon.ico",         # 网站图标
        
        # 第三方回调
        "/api/callback/",       # 第三方回调接口
        
        # 文件上传下载（公开）
        "/api/upload/public/",  # 公开上传
        "/api/download/public/",# 公开下载
    }
    
    # ==================== 正则匹配路径 ====================
    # 使用正则表达式匹配的免鉴权路径
    REGEX_PATTERNS: Set[Pattern] = {
        # 图片验证码（支持带参数的路径）
        re.compile(r"^/api/captchaImage(/.*)?$"),
        
        # 短信验证码
        re.compile(r"^/api/sms/code(/.*)?$"),
        
        # 邮箱验证码
        re.compile(r"^/api/email/code(/.*)?$"),
        
        # 公开查询接口
        re.compile(r"^/api/public/.*$"),
    }
    
    # ==================== 方法级路径配置 ====================
    # 特定HTTP方法的免鉴权路径
    # {method: {paths}}
    METHOD_PATHS: Dict[str, Set[str]] = {
        "GET": {
            "/api/version",             # 版本查询
            "/api/status",              # 状态查询
            "/api/time",                # 时间查询
        },
        "POST": {
            "/api/auth/login",          # 登录
            "/api/auth/logout",         # 登出
            "/api/captchaImage",        # 获取验证码
            "/api/sms/send",            # 发送短信
            "/api/email/send",          # 发送邮件
        },
    }
    
    # ==================== 服务级白名单配置 ====================
    # 特定服务的所有接口都免鉴权（谨慎使用）
    PUBLIC_SERVICES: Set[str] = {
        # "public-service",  # 公共服务（示例）
    }
    
    @classmethod
    def is_whitelisted(cls, path: str, method: str = "GET") -> bool:
        """
        判断路径是否在白名单中
        
        Args:
            path: 请求路径（如 /api/auth/login）
            method: HTTP方法（GET/POST/PUT/DELETE等）
            
        Returns:
            True: 路径在白名单中，免鉴权
            False: 路径不在白名单中，需要鉴权
        """
        # 1. 检查精确匹配
        if path in cls.EXACT_PATHS:
            return True
        
        # 2. 检查前缀匹配
        for prefix in cls.PREFIX_PATHS:
            if path.startswith(prefix):
                return True
        
        # 3. 检查正则匹配
        for pattern in cls.REGEX_PATTERNS:
            if pattern.match(path):
                return True
        
        # 4. 检查方法级路径配置
        method_upper = method.upper()
        if method_upper in cls.METHOD_PATHS:
            if path in cls.METHOD_PATHS[method_upper]:
                return True
        
        return False
    
    @classmethod
    def add_exact_path(cls, path: str):
        """
        添加精确匹配路径
        
        Args:
            path: 要添加的路径
        """
        cls.EXACT_PATHS.add(path)
    
    @classmethod
    def add_prefix_path(cls, prefix: str):
        """
        添加前缀匹配路径
        
        Args:
            prefix: 要添加的路径前缀
        """
        # 确保前缀以/开头
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        cls.PREFIX_PATHS.add(prefix)
    
    @classmethod
    def add_regex_pattern(cls, pattern: str):
        """
        添加正则匹配模式
        
        Args:
            pattern: 正则表达式字符串
        """
        cls.REGEX_PATTERNS.add(re.compile(pattern))
    
    @classmethod
    def add_method_path(cls, method: str, path: str):
        """
        添加方法级路径配置
        
        Args:
            method: HTTP方法
            path: 路径
        """
        method_upper = method.upper()
        if method_upper not in cls.METHOD_PATHS:
            cls.METHOD_PATHS[method_upper] = set()
        cls.METHOD_PATHS[method_upper].add(path)
