# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: inventory_flow_service.py
# @Software: PyCharm
# @Desc : 业务服务

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from dao.inventory_flow_dao import InventoryFlowDao
from schemas.common_schema import PageResponseModel
from schemas.inventory_flow_schema import InventoryFlowModel, InventoryFlowQueryModel

class InventoryFlowService:
    @classmethod
    async def get_flow_list(cls, db: AsyncSession, query_model: InventoryFlowQueryModel) -> PageResponseModel:
        flows, total = await InventoryFlowDao.get_flow_list(db, query_model)
        flow_models = [InventoryFlowModel.model_validate(f) for f in flows]
        return PageResponseModel(
            rows=flow_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def get_flow_by_source(cls, db: AsyncSession, source_type: str, source_id: int) -> List[InventoryFlowModel]:
        flows = await InventoryFlowDao.get_flow_by_source(db, source_type, source_id)
        return [InventoryFlowModel.model_validate(f) for f in flows]