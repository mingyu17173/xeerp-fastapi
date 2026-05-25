# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: category_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from core.get_db import get_db
from schemas.category_schema import (
    AddProductCategoryModel,
    DeleteProductCategoryModel,
    EditProductCategoryModel,
    ProductCategoryModel,
    ProductCategoryPageQueryModel,
)
from schemas.common_schema import CrudResponseModel
from service.category_service import ProductCategoryService
from utils.response_util import ResponseUtil


categoryController = APIRouter()


@categoryController.get('/list', response_model=CrudResponseModel)
async def get_category_list(
    request: Request,
    category_name: Optional[str] = None,
    category_code: Optional[str] = None,
    parent_id: Optional[int] = None,
    status: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品分类列表（分页）
    """
    query_model = ProductCategoryPageQueryModel(
        category_name=category_name,
        category_code=category_code,
        parent_id=parent_id,
        status=status,
        page_num=page_num,
        page_size=page_size,
    )
    categories, total = await ProductCategoryService.get_category_list_services(query_db, query_model)
    return ResponseUtil.success(data=categories, total=total)


@categoryController.get('/all', response_model=CrudResponseModel)
async def get_all_categories(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取所有启用的商品分类列表（不分页）
    """
    categories = await ProductCategoryService.get_all_categories_services(query_db)
    return ResponseUtil.success(data=categories)


@categoryController.get('/tree', response_model=CrudResponseModel)
async def get_category_tree(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品分类树形结构
    """
    tree = await ProductCategoryService.get_category_tree_services(query_db)
    return ResponseUtil.success(data=tree)


@categoryController.get('/{category_id}', response_model=CrudResponseModel)
async def get_category_detail(
    request: Request,
    category_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品分类详情
    """
    category = await ProductCategoryService.get_category_detail_services(query_db, category_id)
    if category:
        return ResponseUtil.success(model_content=category)
    return ResponseUtil.failure(msg='分类不存在')


@categoryController.post('', response_model=CrudResponseModel)
async def add_category(
    request: Request,
    add_model: AddProductCategoryModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    新增商品分类
    """
    result = await ProductCategoryService.add_category_services(request, query_db, add_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@categoryController.put('', response_model=CrudResponseModel)
async def edit_category(
    request: Request,
    edit_model: EditProductCategoryModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    编辑商品分类
    """
    result = await ProductCategoryService.edit_category_services(request, query_db, edit_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@categoryController.delete('/{category_id}', response_model=CrudResponseModel)
async def delete_category(
    request: Request,
    category_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    删除商品分类
    """
    result = await ProductCategoryService.delete_category_services(request, query_db, category_id)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@categoryController.delete('/batch/{category_ids}', response_model=CrudResponseModel)
async def batch_delete_category(
    request: Request,
    category_ids: str,
    query_db: AsyncSession = Depends(get_db),
):
    """
    批量删除商品分类
    """
    delete_model = DeleteProductCategoryModel(category_ids=category_ids)
    result = await ProductCategoryService.batch_delete_category_services(request, query_db, delete_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)