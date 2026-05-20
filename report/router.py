from fastapi import APIRouter
from api.v1 import report_router

report_router = APIRouter()
report_router.include_router(report_router)