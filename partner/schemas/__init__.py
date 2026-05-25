# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 数据模式

from schemas.partner import (
    PartnerModel, AddPartnerModel, EditPartnerModel, PartnerPageQueryModel
)

__all__ = ['PartnerModel', 'AddPartnerModel', 'EditPartnerModel', 'PartnerPageQueryModel']