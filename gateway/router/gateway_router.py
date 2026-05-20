from fastapi import APIRouter, Request, HTTPException
import httpx
from core.env import AppConfig
from core.limiter import limiter
from typing import Dict

router = APIRouter()

service_routes: Dict[str, str] = {
    "/system": AppConfig.system_service_url,
    "/api/user": AppConfig.system_service_url,
    "/api/role": AppConfig.system_service_url,
    "/api/dept": AppConfig.system_service_url,
    "/api/menu": AppConfig.system_service_url,
    "/api/auth": AppConfig.system_service_url,
    "/api/config": AppConfig.system_service_url,
    
    "/product": AppConfig.product_service_url,
    "/api/product": AppConfig.product_service_url,
    
    "/stock": AppConfig.stock_service_url,
    "/api/stock": AppConfig.stock_service_url,
    
    "/production": AppConfig.production_service_url,
    "/api/production": AppConfig.production_service_url,
    
    "/report": AppConfig.report_service_url,
    "/api/report": AppConfig.report_service_url,
}

async def get_target_service(path: str) -> str:
    """
    根据路径匹配目标服务
    """
    for route_prefix, service_url in service_routes.items():
        if path.startswith(route_prefix):
            return service_url
    return None

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@limiter.limit(f"{AppConfig.rate_limit_requests}/{AppConfig.rate_limit_window_seconds}seconds")
async def proxy_request(request: Request, path: str):
    """
    路由转发代理
    """
    target_service = await get_target_service(f"/{path}")
    
    if not target_service:
        raise HTTPException(status_code=404, detail="未找到对应的服务")
    
    url = f"{target_service}/{path}"
    
    headers = {k: v for k, v in request.headers.items() if k != "host"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=await request.body(),
                timeout=30
            )
            
            return httpx.Response(
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content
            )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"服务不可用: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"网关错误: {str(e)}")