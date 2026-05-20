from fastapi import APIRouter
from api.v1 import (
    bom_router,
    production_plan_router,
    production_issue_router,
    production_receipt_router,
    production_return_router,
    production_scrap_router
)

production_router = APIRouter()

production_router.include_router(bom_router)
production_router.include_router(production_plan_router)
production_router.include_router(production_issue_router)
production_router.include_router(production_receipt_router)
production_router.include_router(production_return_router)
production_router.include_router(production_scrap_router)