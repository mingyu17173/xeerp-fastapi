from fastapi import APIRouter
from api.v1 import warehouse_router, inventory_router

stock_router = APIRouter()

stock_router.include_router(warehouse_router)
stock_router.include_router(inventory_router)