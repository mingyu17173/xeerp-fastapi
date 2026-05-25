# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 数据访问层

from dao.warehouse_dao import WarehouseDao
from dao.inventory_dao import InventoryDao
from dao.inventory_flow_dao import InventoryFlowDao

__all__ = ['WarehouseDao', 'InventoryDao', 'InventoryFlowDao']