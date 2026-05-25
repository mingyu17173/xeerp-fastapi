# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: unit_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from core.get_db import get_db
from schemas.common_schema import CrudResponseModel
from schemas.unit_schema import (
    AddProductUnitModel,
    DeleteProductUnitModel,
    EditProductUnitModel,
    ProductUnitModel,
    ProductUnitPageQueryModel,
)
from service.unit_service import ProductUnitService
from utils.response_util import ResponseUtil


unitController = APIRouter()


@unitController.get('/list', response_model=CrudResponseModel)
async def get_unit_list(
    request: Request,
    unit_name: Optional[str] = None,
    unit_code: Optional[str] = None,
    status: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品单位列表（分页）
    """
    query_model = ProductUnitPageQueryModel(
        unit_name=unit_name,
        unit_code=unit_code,
        status=status,
        page_num=page_num,
        page_size=page_size,
    )
    units, total = await ProductUnitService.get_unit_list_services(query_db, query_model)
    return ResponseUtil.success(data=units, total=total)


@unitController.get('/all', response_model=CrudResponseModel)
async def get_all_units(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取所有启用的商品单位列表（不分页）
    """
    units = await ProductUnitService.get_all_units_services(query_db)
    return ResponseUtil.success(data=units)


@unitController.get('/{unit_id}', response_model=CrudResponseModel)
async def get_unit_detail(
    request: Request,
    unit_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品单位详情
    """
    unit = await ProductUnitService.get_unit_detail_services(query_db, unit_id)
    if unit:
        return ResponseUtil.success(model_content=unit)
    return ResponseUtil.failure(msg='单位不存在')


@unitController.post('', response_model=CrudResponseModel)
async def add_unit(
    request: Request,
    add_model: AddProductUnitModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    新增商品单位
    """
    result = await ProductUnitService.add_unit_services(request, query_db, add_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@unitController.put('', response_model=CrudResponseModel)
async def edit_unit(
    request: Request,
    edit_model: EditProductUnitModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    编辑商品单位
    """
    result = await ProductUnitService.edit_unit_services(request, query_db, edit_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@unitController.delete('/{unit_id}', response_model=CrudResponseModel)
async def delete_unit(
    request: Request,
    unit_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    删除商品单位
    """
    result = await ProductUnitService.delete_unit_services(request, query_db, unit_id)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@unitController.delete('/batch/{unit_ids}', response_model=CrudResponseModel)
async def batch_delete_unit(
    request: Request,
    unit_ids: str,
    query_db: AsyncSession = Depends(get_db),
):
    """
    批量删除商品单位
    """
    delete_model = DeleteProductUnitModel(unit_ids=unit_ids)
    result = await ProductUnitService.batch_delete_unit_services(request, query_db, delete_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)