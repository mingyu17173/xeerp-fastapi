# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: gateway_router.py
# @Software: PyCharm
# @Desc : 模块文件

"""
Gateway Service Router
网关服务路由模块
"""

from typing import Dict, Optional
from fastapi import APIRouter, Request, HTTPException
import httpx
from core.env import AppConfig
from core.limiter import limiter
from core.logger import logger
from core.consul_discovery import ConsulServiceDiscovery
from utils.consul_util import SERVICE_CONFIG

router = APIRouter()

# ==================== 服务路由配置 ====================
# 路径前缀 -> 服务名称映射
service_routes: Dict[str, str] = {
    # ==================== 系统服务 ====================
    "/system": "system-service",
    "/api/user": "system-service",
    "/api/role": "system-service",
    "/api/dept": "system-service",
    "/api/menu": "system-service",
    "/api/auth": "system-service",
    "/api/config": "system-service",
    "/api/captcha": "system-service",
    "/api/captchaImage": "system-service",
    "/api/dict": "system-service",
    "/api/log": "system-service",
    "/api/notice": "system-service",
    "/api/login": "system-service",
    "/api/logout": "system-service",
    
    # ==================== 商品服务 ====================
    "/product": "product-service",
    "/api/product": "product-service",
    
    # ==================== 库存服务 ====================
    "/stock": "stock-service",
    "/api/stock": "stock-service",
    
    # ==================== 生产服务 ====================
    "/production": "production-service",
    "/api/production": "production-service",
    
    # ==================== 报表服务 ====================
    "/report": "report-service",
    "/api/report": "report-service",
    
    # ==================== 审批流服务 ====================
    "/approval": "approval-service",
    "/api/approval": "approval-service",
    
    # ==================== 往来单位服务 ====================
    "/partner": "partner-service",
    "/api/partner": "partner-service",
    
    # ==================== 订单中心服务 ====================
    "/order": "order-service",
    "/api/order": "order-service",
    
    # ==================== 采购中心服务 ====================
    "/purchase": "purchase-service",
    "/api/purchase": "purchase-service",
    
    # ==================== 销售服务 ====================
    "/sales": "sales-service",
    "/api/sales": "sales-service",
    
    # ==================== 公共服务 ====================
    "/api/public": "system-service",
    "/api/common": "system-service",
}

# ==================== 路径转换映射 ====================
# 特殊路径转换规则（用于调整路径格式）
path_mappings: Dict[str, str] = {
    # 验证码接口
    "/api/captchaImage": "/captchaImage",
    
    # 认证接口
    "/api/login": "/login",
    "/api/logout": "/logout",
}

# ==================== 公共接口映射 ====================
# 公共接口（免鉴权）直接映射到对应服务
public_api_routes: Dict[str, str] = {
    "/api/auth/login": "system-service",
    "/api/auth/logout": "system-service",
    "/api/captchaImage": "system-service",
    "/api/sms/code": "system-service",
    "/api/email/code": "system-service",
    "/api/public/version": "system-service",
    "/api/public/config": "system-service",
}


async def get_target_service(path: str) -> Optional[str]:
    """
    根据路径匹配目标服务（从Consul获取或使用降级URL）
    
    Args:
        path: 请求路径
        
    Returns:
        目标服务URL，如 http://127.0.0.1:8001
    """
    # 查找匹配的服务（按前缀长度排序，优先匹配更长的前缀）
    sorted_routes = sorted(service_routes.items(), key=lambda x: -len(x[0]))
    for route_prefix, service_name in sorted_routes:
        if path.startswith(route_prefix):
            # 从Consul获取服务URL
            url = ConsulServiceDiscovery.get_service_url(service_name)
            if url:
                return url
            
            # 如果Consul不可用，使用配置文件中的降级URL
            fallback_url = get_fallback_url(service_name)
            if fallback_url:
                logger.warning(f"⚠️ Consul不可用，使用降级URL: {fallback_url}")
                return fallback_url
            
            return None
    
    return None


def get_fallback_url(service_name: str) -> Optional[str]:
    """
    获取降级服务URL
    
    Args:
        service_name: 服务名称
        
    Returns:
        降级URL
    """
    # 从配置映射中获取
    for key, config in SERVICE_CONFIG.items():
        if config["service_name"] == service_name:
            return f"http://127.0.0.1:{config['port']}"
    
    # 从环境配置中获取
    config_attr = f"{service_name.replace('-', '_')}_url"
    if hasattr(AppConfig, config_attr):
        return getattr(AppConfig, config_attr)
    
    return None


def transform_path(path: str) -> str:
    """
    转换路径，处理特殊路径映射和服务前缀去除
    
    Args:
        path: 原始路径（如 /api/user/list）
        
    Returns:
        转换后的路径（如 /user/list）
    """
    # 1. 先处理精确匹配的特殊路径映射
    if path in path_mappings:
        return path_mappings[path]
    
    # 2. 处理公共接口路径映射
    if path in public_api_routes:
        # 公共接口通常需要去除 /api 前缀
        if path.startswith("/api/"):
            return path[4:]  # 去除 /api
        return path
    
    # 3. 按前缀长度排序，优先匹配更长的前缀
    sorted_routes = sorted(service_routes.items(), key=lambda x: -len(x[0]))
    
    # 4. 去除服务前缀
    for route_prefix, _ in sorted_routes:
        if path.startswith(route_prefix):
            # 移除前缀，保留剩余部分
            remaining_path = path[len(route_prefix):]
            # 如果剩余部分为空或不以/开头，添加/
            if not remaining_path or not remaining_path.startswith('/'):
                remaining_path = '/' + remaining_path if remaining_path else '/'
            return remaining_path
    
    return path


def is_public_api(path: str, method: str = "GET") -> bool:
    """
    判断是否为公共接口
    
    Args:
        path: 请求路径
        method: HTTP方法
        
    Returns:
        True: 公共接口（免鉴权）
        False: 需要鉴权的接口
    """
    # 检查公共接口直接映射
    if path in public_api_routes:
        return True
    
    # 检查公共路径前缀
    public_prefixes = ["/api/public/", "/api/common/", "/api/captcha", "/api/auth/"]
    for prefix in public_prefixes:
        if path.startswith(prefix):
            return True
    
    return False


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@limiter.limit(f"{AppConfig.rate_limit_requests}/{AppConfig.rate_limit_window_seconds}seconds")
async def proxy_request(request: Request, path: str):
    """
    路由转发代理
    
    将请求转发到对应的微服务
    """
    full_path = f"/{path}"
    
    # 查找目标服务
    target_service = await get_target_service(full_path)
    if not target_service:
        logger.warning(f"❌ 未找到对应的服务: {full_path}")
        raise HTTPException(status_code=404, detail={"code": 404, "message": "未找到对应的服务"})
    
    # 路径转换
    transformed_path = transform_path(full_path)
    url = f"{target_service}{transformed_path}"
    
    # 构建请求头（移除host头）
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    # 添加追踪信息
    headers["X-Gateway"] = "xeerp-gateway"
    headers["X-Trace-Id"] = getattr(request.state, "request_id", "unknown")
    
    logger.info(f"📤 转发请求: {request.method} {full_path} -> {url}")
    
    try:
        async with httpx.AsyncClient(timeout=AppConfig.request_timeout) as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=await request.body(),
                params=request.query_params,
                follow_redirects=False
            )
            
            # 构建响应
            return httpx.Response(
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content
            )
    
    except httpx.HTTPError as e:
        logger.error(f"❌ 服务不可用: {url}, 错误: {str(e)}")
        raise HTTPException(status_code=503, detail={"code": 503, "message": f"服务不可用: {str(e)}"})
    except Exception as e:
        logger.error(f"❌ 网关错误: {url}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail={"code": 500, "message": f"网关错误: {str(e)}"})