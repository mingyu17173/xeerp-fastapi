# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: unit_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional


class ProductUnitModel(BaseModel):
    """
    商品单位信息模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    unit_id: Optional[int] = Field(default=None, description='单位ID')
    unit_name: Optional[str] = Field(default=None, description='单位名称')
    unit_code: Optional[str] = Field(default=None, description='单位编码')
    sort_order: Optional[int] = Field(default=None, description='排序号')
    status: Optional[str] = Field(default=None, description='状态（0正常 1停用）')
    is_delete: Optional[str] = Field(default=None, description='删除标志')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')


class ProductUnitQueryModel(ProductUnitModel):
    """
    商品单位查询模型
    """
    pass


class ProductUnitPageQueryModel(ProductUnitModel):
    """
    商品单位分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class AddProductUnitModel(BaseModel):
    """
    新增商品单位模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    unit_name: str = Field(description='单位名称')
    unit_code: str = Field(description='单位编码')
    sort_order: int = Field(default=0, description='排序号')
    status: str = Field(default='0', description='状态（0正常 1停用）')
    remark: Optional[str] = Field(default=None, description='备注')


class EditProductUnitModel(AddProductUnitModel):
    """
    编辑商品单位模型
    """
    unit_id: int = Field(description='单位ID')


class DeleteProductUnitModel(BaseModel):
    """
    删除商品单位模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    unit_ids: str = Field(description='需要删除的单位ID，多个用逗号分隔')