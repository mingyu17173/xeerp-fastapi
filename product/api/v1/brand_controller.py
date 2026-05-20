from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from core.get_db import get_db
from schemas.brand_schema import (
    AddProductBrandModel,
    DeleteProductBrandModel,
    EditProductBrandModel,
    ProductBrandModel,
    ProductBrandPageQueryModel,
)
from schemas.common_schema import CrudResponseModel
from service.brand_service import ProductBrandService
from utils.response_util import ResponseUtil


brandController = APIRouter()


@brandController.get('/list', response_model=CrudResponseModel)
async def get_brand_list(
    request: Request,
    brand_name: Optional[str] = None,
    brand_code: Optional[str] = None,
    status: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品品牌列表（分页）
    """
    query_model = ProductBrandPageQueryModel(
        brand_name=brand_name,
        brand_code=brand_code,
        status=status,
        page_num=page_num,
        page_size=page_size,
    )
    brands, total = await ProductBrandService.get_brand_list_services(query_db, query_model)
    return ResponseUtil.success(data=brands, total=total)


@brandController.get('/all', response_model=CrudResponseModel)
async def get_all_brands(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取所有启用的商品品牌列表（不分页）
    """
    brands = await ProductBrandService.get_all_brands_services(query_db)
    return ResponseUtil.success(data=brands)


@brandController.get('/{brand_id}', response_model=CrudResponseModel)
async def get_brand_detail(
    request: Request,
    brand_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品品牌详情
    """
    brand = await ProductBrandService.get_brand_detail_services(query_db, brand_id)
    if brand:
        return ResponseUtil.success(model_content=brand)
    return ResponseUtil.failure(msg='品牌不存在')


@brandController.post('', response_model=CrudResponseModel)
async def add_brand(
    request: Request,
    add_model: AddProductBrandModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    新增商品品牌
    """
    result = await ProductBrandService.add_brand_services(request, query_db, add_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@brandController.put('', response_model=CrudResponseModel)
async def edit_brand(
    request: Request,
    edit_model: EditProductBrandModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    编辑商品品牌
    """
    result = await ProductBrandService.edit_brand_services(request, query_db, edit_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@brandController.delete('/{brand_id}', response_model=CrudResponseModel)
async def delete_brand(
    request: Request,
    brand_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    删除商品品牌
    """
    result = await ProductBrandService.delete_brand_services(request, query_db, brand_id)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@brandController.delete('/batch/{brand_ids}', response_model=CrudResponseModel)
async def batch_delete_brand(
    request: Request,
    brand_ids: str,
    query_db: AsyncSession = Depends(get_db),
):
    """
    批量删除商品品牌
    """
    delete_model = DeleteProductBrandModel(brand_ids=brand_ids)
    result = await ProductBrandService.batch_delete_brand_services(request, query_db, delete_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)