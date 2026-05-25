# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: region_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from core.annotation.pydantic_annotation import as_query




class RegionModel(BaseModel):
    """
    地区表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='')
    code: Optional[str] = Field(default=None, description='统计用区划代码')
    name: Optional[str] = Field(default=None, description='名称')
    parent_id: Optional[int] = Field(default=None, description='父级')
    level: Optional[bytes] = Field(default=None, description='级别')






class RegionQueryModel(RegionModel):
    """
    地区不分页查询模型
    """
    pass


@as_query
class RegionPageQueryModel(RegionQueryModel):
    """
    地区分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteRegionModel(BaseModel):
    """
    删除地区模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的')
