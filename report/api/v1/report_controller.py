from fastapi import APIRouter, Depends
from service.report_service import ReportService
from schemas.report_schema import (
    ProductionProgressReport,
    IssueDetailReport,
    ReceiptCostReport,
    InventoryLedgerReport,
    ReportQueryModel
)

router = APIRouter(prefix='/report', tags=['报表管理'])

@router.get('/production-progress', response_model=ProductionProgressReport)
async def get_production_progress_report(query: ReportQueryModel = Depends()):
    return await ReportService.get_production_progress_report(query)

@router.get('/issue-detail', response_model=IssueDetailReport)
async def get_issue_detail_report(query: ReportQueryModel = Depends()):
    return await ReportService.get_issue_detail_report(query)

@router.get('/receipt-cost', response_model=ReceiptCostReport)
async def get_receipt_cost_report(query: ReportQueryModel = Depends()):
    return await ReportService.get_receipt_cost_report(query)

@router.get('/inventory-ledger', response_model=InventoryLedgerReport)
async def get_inventory_ledger_report(query: ReportQueryModel = Depends()):
    return await ReportService.get_inventory_ledger_report(query)