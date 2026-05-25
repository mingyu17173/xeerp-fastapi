# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: brand_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional


class ProductBrandModel(BaseModel):
    """
    商品品牌信息模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    brand_id: Optional[int] = Field(default=None, description='品牌ID')
    brand_name: Optional[str] = Field(default=None, description='品牌名称')
    brand_code: Optional[str] = Field(default=None, description='品牌编码')
    brand_logo: Optional[str] = Field(default=None, description='品牌logo路径')
    sort_order: Optional[int] = Field(default=None, description='排序号')
    status: Optional[str] = Field(default=None, description='状态（0正常 1停用）')
    is_delete: Optional[str] = Field(default=None, description='删除标志')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')


class ProductBrandQueryModel(ProductBrandModel):
    """
    商品品牌查询模型
    """
    pass


class ProductBrandPageQueryModel(ProductBrandModel):
    """
    商品品牌分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class AddProductBrandModel(BaseModel):
    """
    新增商品品牌模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    brand_name: str = Field(description='品牌名称')
    brand_code: str = Field(description='品牌编码')
    brand_logo: Optional[str] = Field(default=None, description='品牌logo路径')
    sort_order: int = Field(default=0, description='排序号')
    status: str = Field(default='0', description='状态（0正常 1停用）')
    remark: Optional[str] = Field(default=None, description='备注')


class EditProductBrandModel(AddProductBrandModel):
    """
    编辑商品品牌模型
    """
    brand_id: int = Field(description='品牌ID')


class DeleteProductBrandModel(BaseModel):
    """
    删除商品品牌模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    brand_ids: str = Field(description='需要删除的品牌ID，多个用逗号分隔')