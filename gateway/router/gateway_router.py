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
from core.nacos_discovery import NacosServiceDiscovery

router = APIRouter()

# 服务路由配置（路径 -> 服务名称映射）
service_routes: Dict[str, str] = {
    "/system": "system-service",
    "/api/user": "system-service",
    "/api/role": "system-service",
    "/api/dept": "system-service",
    "/api/menu": "system-service",
    "/api/auth": "system-service",
    "/api/config": "system-service",
    "/api/captchaImage": "system-service",
    "/api/dict": "system-service",
    "/api/log": "system-service",
    "/api/notice": "system-service",
    
    "/product": "product-service",
    "/api/product": "product-service",
    
    "/stock": "stock-service",
    "/api/stock": "stock-service",
    
    "/production": "production-service",
    "/api/production": "production-service",
    
    "/report": "report-service",
    "/api/report": "report-service",
    
    "/approval": "approval-service",
    "/api/approval": "approval-service",
    
    "/partner": "partner-service",
    "/api/partner": "partner-service",
    
    "/order": "order-service",
    "/api/order": "order-service",
    
    "/purchase": "purchase-service",
    "/api/purchase": "purchase-service",
    
    "/sales": "sales-service",
    "/api/sales": "sales-service",
}

# 降级服务URL配置
fallback_service_urls: Dict[str, str] = {
    "system-service": AppConfig.system_service_url,
    "product-service": AppConfig.product_service_url,
    "stock-service": AppConfig.stock_service_url,
    "production-service": AppConfig.production_service_url,
    "report-service": AppConfig.report_service_url,
    "approval-service": AppConfig.approval_service_url,
    "partner-service": AppConfig.partner_service_url,
    "order-service": AppConfig.order_service_url,
    "purchase-service": AppConfig.purchase_service_url,
    "sales-service": AppConfig.sales_service_url,
}

# 路径转换映射（处理特殊路径）
path_mappings: Dict[str, str] = {
    "/api/captchaImage": "/captchaImage",
}

async def get_target_service(path: str) -> Optional[str]:
    """
    根据路径匹配目标服务（从Nacos获取或使用降级URL）
    """
    for route_prefix, service_name in service_routes.items():
        if path.startswith(route_prefix):
            # 从Nacos获取服务URL，支持降级
            fallback_url = fallback_service_urls.get(service_name)
            return NacosServiceDiscovery.get_service_url_with_fallback(
                service_name,
                fallback_url
            )
    return None

def transform_path(path: str) -> str:
    """
    转换路径，处理特殊路径映射
    """
    return path_mappings.get(path, path)

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@limiter.limit(f"{AppConfig.rate_limit_requests}/{AppConfig.rate_limit_window_seconds}seconds")
async def proxy_request(request: Request, path: str):
    """
    路由转发代理
    """
    full_path = f"/{path}"
    
    # 查找目标服务
    target_service = await get_target_service(full_path)
    if not target_service:
        logger.warning(f"未找到对应的服务: {full_path}")
        raise HTTPException(status_code=404, detail={"code": 404, "message": "未找到对应的服务"})
    
    # 路径转换
    transformed_path = transform_path(full_path)
    url = f"{target_service}{transformed_path}"
    
    # 构建请求头（移除host头）
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    # 添加追踪信息
    headers["X-Gateway"] = "xeerp-gateway"
    
    logger.info(f"转发请求: {request.method} {full_path} -> {url}")
    
    try:
        async with httpx.AsyncClient(timeout=AppConfig.request_timeout) as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=await request.body(),
                follow_redirects=False
            )
            
            # 构建响应
            return httpx.Response(
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content
            )
    
    except httpx.HTTPError as e:
        logger.error(f"服务不可用: {url}, 错误: {str(e)}")
        raise HTTPException(status_code=503, detail={"code": 503, "message": f"服务不可用: {str(e)}"})
    except Exception as e:
        logger.error(f"网关错误: {url}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail={"code": 500, "message": f"网关错误: {str(e)}"})