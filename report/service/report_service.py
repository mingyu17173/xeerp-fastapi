# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: report_service.py
# @Software: PyCharm
# @Desc : 业务服务

from typing import List, Dict
from clients.production_client import ProductionClient
from clients.stock_client import StockClient
from schemas.report_schema import (
    ProductionProgressReport, ProductionProgressItem,
    IssueDetailReport, IssueDetailItem,
    ReceiptCostReport, ReceiptCostItem,
    InventoryLedgerReport, InventoryLedgerItem,
    ReportQueryModel
)

class ReportService:
    @classmethod
    async def get_production_progress_report(cls, query: ReportQueryModel = None) -> ProductionProgressReport:
        production_client = ProductionClient()
        
        try:
            status, data = await production_client.get_production_plan_list()
            
            if status != 200:
                return ProductionProgressReport(
                    total_plans=0,
                    completed_plans=0,
                    in_progress_plans=0,
                    pending_plans=0,
                    total_quantity=0,
                    finished_quantity=0,
                    overall_progress=0,
                    details=[]
                )
            
            rows = data.get('data', {}).get('rows', [])
            plan_items = []
            total_plans = 0
            completed_plans = 0
            in_progress_plans = 0
            pending_plans = 0
            total_quantity = 0
            finished_quantity = 0
            
            status_map = {'0': '待生产', '1': '生产中', '2': '已完成', '3': '已取消'}
            
            for row in rows:
                progress = (row['finished_quantity'] / row['plan_quantity']) * 100 if row['plan_quantity'] > 0 else 0
                
                item = ProductionProgressItem(
                    plan_id=row['plan_id'],
                    plan_code=row['plan_code'],
                    product_name=row.get('product_name', ''),
                    plan_quantity=row['plan_quantity'],
                    finished_quantity=row['finished_quantity'],
                    progress=round(progress, 2),
                    status=row['status'],
                    status_text=status_map.get(row['status'], '未知'),
                    start_date=row['start_date'],
                    end_date=row['end_date']
                )
                plan_items.append(item)
                
                total_plans += 1
                total_quantity += row['plan_quantity']
                finished_quantity += row['finished_quantity']
                
                if row['status'] == '0':
                    pending_plans += 1
                elif row['status'] == '1':
                    in_progress_plans += 1
                elif row['status'] == '2':
                    completed_plans += 1
            
            overall_progress = (finished_quantity / total_quantity) * 100 if total_quantity > 0 else 0
            
            return ProductionProgressReport(
                total_plans=total_plans,
                completed_plans=completed_plans,
                in_progress_plans=in_progress_plans,
                pending_plans=pending_plans,
                total_quantity=total_quantity,
                finished_quantity=finished_quantity,
                overall_progress=round(overall_progress, 2),
                details=plan_items
            )
        finally:
            await production_client.close()

    @classmethod
    async def get_issue_detail_report(cls, query: ReportQueryModel = None) -> IssueDetailReport:
        production_client = ProductionClient()
        
        try:
            status, data = await production_client.get_production_issue_list()
            
            if status != 200:
                return IssueDetailReport(
                    total_issues=0,
                    issued_issues=0,
                    total_material_value=0,
                    details=[]
                )
            
            rows = data.get('data', {}).get('rows', [])
            issue_items = []
            total_issues = 0
            issued_issues = 0
            total_material_value = 0
            
            status_map = {'0': '待审核', '1': '已审核', '2': '已发料', '3': '已取消'}
            
            for row in rows:
                for item in row.get('items', []):
                    issue_item = IssueDetailItem(
                        issue_id=row['issue_id'],
                        issue_code=row['issue_code'],
                        plan_code=row.get('plan_code', ''),
                        material_id=item['material_id'],
                        material_name=item.get('material_name', ''),
                        plan_quantity=item['plan_quantity'],
                        actual_quantity=item['actual_quantity'],
                        unit=item.get('unit', ''),
                        warehouse_id=row['warehouse_id'],
                        status=row['status'],
                        status_text=status_map.get(row['status'], '未知'),
                        create_time=row['create_time']
                    )
                    issue_items.append(issue_item)
                
                total_issues += 1
                if row['status'] == '2':
                    issued_issues += 1
            
            return IssueDetailReport(
                total_issues=total_issues,
                issued_issues=issued_issues,
                total_material_value=total_material_value,
                details=issue_items
            )
        finally:
            await production_client.close()

    @classmethod
    async def get_receipt_cost_report(cls, query: ReportQueryModel = None) -> ReceiptCostReport:
        production_client = ProductionClient()
        
        try:
            status, data = await production_client.get_production_receipt_list()
            
            if status != 200:
                return ReceiptCostReport(
                    total_receipts=0,
                    received_receipts=0,
                    total_quantity=0,
                    total_cost=0,
                    average_cost=0,
                    details=[]
                )
            
            rows = data.get('data', {}).get('rows', [])
            receipt_items = []
            total_receipts = 0
            received_receipts = 0
            total_quantity = 0
            total_cost = 0
            
            for row in rows:
                receipt_item = ReceiptCostItem(
                    receipt_id=row['receipt_id'],
                    receipt_code=row['receipt_code'],
                    plan_code=row.get('plan_code', ''),
                    product_id=0,
                    product_name=row.get('product_name', ''),
                    quantity=row['quantity'],
                    unit_cost=0,
                    total_cost=0,
                    warehouse_id=row['warehouse_id'],
                    status=row['status'],
                    create_time=row['create_time']
                )
                receipt_items.append(receipt_item)
                
                total_receipts += 1
                total_quantity += row['quantity']
                if row['status'] == '2':
                    received_receipts += 1
            
            average_cost = total_cost / total_quantity if total_quantity > 0 else 0
            
            return ReceiptCostReport(
                total_receipts=total_receipts,
                received_receipts=received_receipts,
                total_quantity=total_quantity,
                total_cost=round(total_cost, 2),
                average_cost=round(average_cost, 2),
                details=receipt_items
            )
        finally:
            await production_client.close()

    @classmethod
    async def get_inventory_ledger_report(cls, query: ReportQueryModel = None) -> InventoryLedgerReport:
        stock_client = StockClient()
        
        try:
            status, data = await stock_client.get_inventory_list(page_size=1000)
            
            if status != 200:
                return InventoryLedgerReport(
                    total_products=0,
                    total_quantity=0,
                    total_warehouses=0,
                    details=[]
                )
            
            rows = data.get('data', {}).get('rows', [])
            warehouse_map = {}
            
            warehouse_status, warehouse_data = await stock_client.get_warehouse_list()
            if warehouse_status == 200:
                for wh in warehouse_data.get('data', {}).get('rows', []):
                    warehouse_map[wh['warehouse_id']] = wh['warehouse_name']
            
            inventory_items = []
            product_ids = set()
            warehouse_ids = set()
            total_quantity = 0
            
            for row in rows:
                inventory_item = InventoryLedgerItem(
                    product_id=row['product_id'],
                    product_name=row.get('product_name', ''),
                    warehouse_id=row['warehouse_id'],
                    warehouse_name=warehouse_map.get(row['warehouse_id'], ''),
                    quantity=row['quantity'],
                    unit=row.get('unit', ''),
                    batch_no=row.get('batch_no'),
                    expire_date=row.get('expire_date')
                )
                inventory_items.append(inventory_item)
                
                product_ids.add(row['product_id'])
                warehouse_ids.add(row['warehouse_id'])
                total_quantity += row['quantity']
            
            return InventoryLedgerReport(
                total_products=len(product_ids),
                total_quantity=total_quantity,
                total_warehouses=len(warehouse_ids),
                details=inventory_items
            )
        finally:
            await stock_client.close()