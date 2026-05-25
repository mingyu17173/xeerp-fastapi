# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_issue_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.get_db import get_db
from service.production_issue_service import ProductionIssueService
from schemas.production_issue_schema import ProductionIssueModel, AddProductionIssueModel, ProductionIssuePageQueryModel
from schemas.common_schema import CrudResponseModel, PageResponseModel
from typing import List

router = APIRouter(prefix='/production/issue', tags=['生产领料'])

@router.get('/{issue_id}', response_model=ProductionIssueModel)
async def get_issue_detail(issue_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionIssueService.get_issue_detail(db, issue_id)

@router.get('/list', response_model=PageResponseModel[ProductionIssueModel])
async def get_issue_list(query: ProductionIssuePageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await ProductionIssueService.get_issue_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_issue(request: Request, add_model: AddProductionIssueModel, db: AsyncSession = Depends(get_db)):
    return await ProductionIssueService.add_issue(request, db, add_model)

@router.post('/{issue_id}/approve', response_model=CrudResponseModel)
async def approve_issue(request: Request, issue_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionIssueService.approve_issue(request, db, issue_id)

@router.post('/{issue_id}/issue', response_model=CrudResponseModel)
async def issue_material(request: Request, issue_id: int, items: List[dict], db: AsyncSession = Depends(get_db)):
    return await ProductionIssueService.issue_material(request, db, issue_id, items)