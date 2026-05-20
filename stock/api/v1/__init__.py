from api.v1.warehouse_controller import router as warehouse_router
from api.v1.inventory_controller import router as inventory_router

__all__ = ['warehouse_router', 'inventory_router']