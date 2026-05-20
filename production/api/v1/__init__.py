from api.v1.bom_controller import router as bom_router
from api.v1.production_plan_controller import router as production_plan_router
from api.v1.production_issue_controller import router as production_issue_router
from api.v1.production_receipt_controller import router as production_receipt_router
from api.v1.production_return_controller import router as production_return_router
from api.v1.production_scrap_controller import router as production_scrap_router

__all__ = [
    'bom_router', 'production_plan_router', 'production_issue_router',
    'production_receipt_router', 'production_return_router', 'production_scrap_router'
]