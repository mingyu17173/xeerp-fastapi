from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from core.get_db import get_db
from schemas.common_schema import CrudResponseModel
from schemas.product_schema import (
    AddProductModel,
    DeleteProductModel,
    EditProductModel,
    ProductModel,
    ProductPageQueryModel,
)
from service.product_service import ProductService
from utils.response_util import ResponseUtil


productController = APIRouter()


@productController.get('/list', response_model=CrudResponseModel)
async def get_product_list(
    request: Request,
    product_name: Optional[str] = None,
    product_code: Optional[str] = None,
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    status: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品列表
    """
    query_model = ProductPageQueryModel(
        product_name=product_name,
        product_code=product_code,
        category_id=category_id,
        brand=brand,
        status=status,
        page_num=page_num,
        page_size=page_size,
    )
    products, total = await ProductService.get_product_list_services(query_db, query_model)
    return ResponseUtil.success(data=products, total=total)


@productController.get('/{product_id}', response_model=CrudResponseModel)
async def get_product_detail(
    request: Request,
    product_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取商品详情
    """
    product = await ProductService.get_product_detail_services(query_db, product_id)
    if product:
        return ResponseUtil.success(model_content=product)
    return ResponseUtil.failure(msg='商品不存在')


@productController.post('', response_model=CrudResponseModel)
async def add_product(
    request: Request,
    add_model: AddProductModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    新增商品
    """
    result = await ProductService.add_product_services(request, query_db, add_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@productController.put('', response_model=CrudResponseModel)
async def edit_product(
    request: Request,
    edit_model: EditProductModel,
    query_db: AsyncSession = Depends(get_db),
):
    """
    编辑商品
    """
    result = await ProductService.edit_product_services(request, query_db, edit_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@productController.delete('/{product_id}', response_model=CrudResponseModel)
async def delete_product(
    request: Request,
    product_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    删除商品
    """
    result = await ProductService.delete_product_services(request, query_db, product_id)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)


@productController.delete('/batch/{product_ids}', response_model=CrudResponseModel)
async def batch_delete_product(
    request: Request,
    product_ids: str,
    query_db: AsyncSession = Depends(get_db),
):
    """
    批量删除商品
    """
    delete_model = DeleteProductModel(product_ids=product_ids)
    result = await ProductService.batch_delete_product_services(request, query_db, delete_model)
    if result.is_success:
        return ResponseUtil.success(msg=result.message)
    return ResponseUtil.failure(msg=result.message)