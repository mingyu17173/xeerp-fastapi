# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: category_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, List


class ProductCategoryModel(BaseModel):
    """
    商品分类信息模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    category_id: Optional[int] = Field(default=None, description='分类ID')
    parent_id: Optional[int] = Field(default=None, description='父分类ID')
    category_name: Optional[str] = Field(default=None, description='分类名称')
    category_code: Optional[str] = Field(default=None, description='分类编码')
    sort_order: Optional[int] = Field(default=None, description='排序号')
    status: Optional[str] = Field(default=None, description='状态（0正常 1停用）')
    is_delete: Optional[str] = Field(default=None, description='删除标志')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')


class ProductCategoryTreeModel(ProductCategoryModel):
    """
    商品分类树形结构模型
    """
    children: Optional[List['ProductCategoryTreeModel']] = Field(default=None, description='子分类列表')


class ProductCategoryQueryModel(ProductCategoryModel):
    """
    商品分类查询模型
    """
    pass


class ProductCategoryPageQueryModel(ProductCategoryModel):
    """
    商品分类分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class AddProductCategoryModel(BaseModel):
    """
    新增商品分类模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    parent_id: Optional[int] = Field(default=0, description='父分类ID（0表示一级分类）')
    category_name: str = Field(description='分类名称')
    category_code: str = Field(description='分类编码')
    sort_order: int = Field(default=0, description='排序号')
    status: str = Field(default='0', description='状态（0正常 1停用）')
    remark: Optional[str] = Field(default=None, description='备注')


class EditProductCategoryModel(AddProductCategoryModel):
    """
    编辑商品分类模型
    """
    category_id: int = Field(description='分类ID')


class DeleteProductCategoryModel(BaseModel):
    """
    删除商品分类模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    category_ids: str = Field(description='需要删除的分类ID，多个用逗号分隔')