# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: production_issue_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import httpx
from dao.production_issue_dao import ProductionIssueDao
from dao.production_plan_dao import ProductionPlanDao
from dao.bom_dao import BomDao
from models.production_issue import SysProductionIssue, SysProductionIssueItem
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.production_issue_schema import ProductionIssueModel, AddProductionIssueModel, ProductionIssuePageQueryModel
from core.production_env import AppConfig

class ProductionIssueService:
    @classmethod
    async def get_issue_detail(cls, db: AsyncSession, issue_id: int) -> Optional[ProductionIssueModel]:
        issue = await ProductionIssueDao.get_issue_by_id(db, issue_id)
        if issue:
            return ProductionIssueModel.model_validate(issue)
        return None

    @classmethod
    async def get_issue_list(cls, db: AsyncSession, query_model: ProductionIssuePageQueryModel) -> PageResponseModel:
        issues, total = await ProductionIssueDao.get_issue_list(db, query_model)
        issue_models = [ProductionIssueModel.model_validate(i) for i in issues]
        return PageResponseModel(
            rows=issue_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_issue(cls, request: Request, db: AsyncSession, add_model: AddProductionIssueModel) -> CrudResponseModel:
        if await ProductionIssueDao.get_issue_by_code(db, add_model.issue_code):
            return CrudResponseModel(is_success=False, message=f"领料单编号 '{add_model.issue_code}' 已存在")

        plan = await ProductionPlanDao.get_plan_by_id(db, add_model.plan_id)
        if not plan:
            return CrudResponseModel(is_success=False, message='生产计划不存在')

        issue = SysProductionIssue(
            issue_code=add_model.issue_code,
            plan_id=add_model.plan_id,
            warehouse_id=add_model.warehouse_id,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        for item in add_model.items:
            issue_item = SysProductionIssueItem(
                material_id=item['material_id'],
                material_name=item.get('material_name'),
                unit=item.get('unit'),
                plan_quantity=item['quantity'],
                actual_quantity=0
            )
            issue.items.append(issue_item)

        await ProductionIssueDao.add_issue(db, issue)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def approve_issue(cls, request: Request, db: AsyncSession, issue_id: int) -> CrudResponseModel:
        issue = await ProductionIssueDao.get_issue_by_id(db, issue_id)
        if not issue:
            return CrudResponseModel(is_success=False, message='领料单不存在')

        if issue.status != '0':
            return CrudResponseModel(is_success=False, message='只能审核待审核状态的领料单')

        await ProductionIssueDao.update_issue_status(db, issue_id, '1', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='审核成功')

    @classmethod
    async def issue_material(cls, request: Request, db: AsyncSession, issue_id: int, items: List[dict]) -> CrudResponseModel:
        issue = await ProductionIssueDao.get_issue_by_id(db, issue_id)
        if not issue:
            return CrudResponseModel(is_success=False, message='领料单不存在')

        if issue.status != '1':
            return CrudResponseModel(is_success=False, message='只能发料已审核的领料单')

        await ProductionIssueDao.update_issue_items_actual(db, issue_id, items)
        
        async with httpx.AsyncClient() as client:
            stock_items = []
            for item in items:
                stock_items.append({
                    'product_id': item['material_id'],
                    'warehouse_id': issue.warehouse_id,
                    'quantity': -item['actual_quantity'],
                    'source_type': 'production',
                    'source_id': issue_id
                })
            
            response = await client.post(f"{AppConfig.stock_service_url}/api/stock/batch-adjust", json=stock_items)
            if response.status_code != 200:
                await db.rollback()
                return CrudResponseModel(is_success=False, message='库存扣减失败')

        await ProductionIssueDao.update_issue_status(db, issue_id, '2', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='发料成功')