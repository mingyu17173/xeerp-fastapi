# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 数据模式

from schemas.bom_schema import BomModel, AddBomModel, EditBomModel, BomPageQueryModel, BomItemModel
from schemas.production_plan_schema import ProductionPlanModel, AddProductionPlanModel, EditProductionPlanModel, ProductionPlanPageQueryModel
from schemas.production_issue_schema import ProductionIssueModel, AddProductionIssueModel, ProductionIssuePageQueryModel, ProductionIssueItemModel
from schemas.production_receipt_schema import ProductionReceiptModel, AddProductionReceiptModel, ProductionReceiptPageQueryModel
from schemas.production_return_schema import ProductionReturnModel, AddProductionReturnModel, ProductionReturnPageQueryModel, ProductionReturnItemModel
from schemas.production_scrap_schema import ProductionScrapModel, AddProductionScrapModel, ProductionScrapPageQueryModel, ProductionScrapItemModel
from schemas.common_schema import CrudResponseModel, PageResponseModel, DeleteModel

__all__ = [
    'BomModel', 'AddBomModel', 'EditBomModel', 'BomPageQueryModel', 'BomItemModel',
    'ProductionPlanModel', 'AddProductionPlanModel', 'EditProductionPlanModel', 'ProductionPlanPageQueryModel',
    'ProductionIssueModel', 'AddProductionIssueModel', 'ProductionIssuePageQueryModel', 'ProductionIssueItemModel',
    'ProductionReceiptModel', 'AddProductionReceiptModel', 'ProductionReceiptPageQueryModel',
    'ProductionReturnModel', 'AddProductionReturnModel', 'ProductionReturnPageQueryModel', 'ProductionReturnItemModel',
    'ProductionScrapModel', 'AddProductionScrapModel', 'ProductionScrapPageQueryModel', 'ProductionScrapItemModel',
    'CrudResponseModel', 'PageResponseModel', 'DeleteModel'
]