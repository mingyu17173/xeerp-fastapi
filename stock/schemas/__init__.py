# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 数据模式

from schemas.warehouse_schema import WarehouseModel, AddWarehouseModel, EditWarehouseModel, WarehousePageQueryModel
from schemas.inventory_schema import InventoryModel, InventoryQueryModel, InventoryAdjustModel
from schemas.inventory_flow_schema import InventoryFlowModel, InventoryFlowQueryModel, InventoryFlowCreateModel
from schemas.common_schema import CrudResponseModel, PageResponseModel, DeleteModel

__all__ = [
    'WarehouseModel', 'AddWarehouseModel', 'EditWarehouseModel', 'WarehousePageQueryModel',
    'InventoryModel', 'InventoryQueryModel', 'InventoryAdjustModel',
    'InventoryFlowModel', 'InventoryFlowQueryModel', 'InventoryFlowCreateModel',
    'CrudResponseModel', 'PageResponseModel', 'DeleteModel'
]