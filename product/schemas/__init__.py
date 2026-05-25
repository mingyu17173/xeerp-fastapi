# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 数据模式

from schemas.product_schema import (
    ProductModel,
    ProductQueryModel,
    ProductPageQueryModel,
    AddProductModel,
    EditProductModel,
    DeleteProductModel
)
from schemas.unit_schema import (
    ProductUnitModel,
    ProductUnitQueryModel,
    ProductUnitPageQueryModel,
    AddProductUnitModel,
    EditProductUnitModel,
    DeleteProductUnitModel
)
from schemas.category_schema import (
    ProductCategoryModel,
    ProductCategoryTreeModel,
    ProductCategoryQueryModel,
    ProductCategoryPageQueryModel,
    AddProductCategoryModel,
    EditProductCategoryModel,
    DeleteProductCategoryModel
)
from schemas.brand_schema import (
    ProductBrandModel,
    ProductBrandQueryModel,
    ProductBrandPageQueryModel,
    AddProductBrandModel,
    EditProductBrandModel,
    DeleteProductBrandModel
)

__all__ = [
    'ProductModel',
    'ProductQueryModel',
    'ProductPageQueryModel',
    'AddProductModel',
    'EditProductModel',
    'DeleteProductModel',
    'ProductUnitModel',
    'ProductUnitQueryModel',
    'ProductUnitPageQueryModel',
    'AddProductUnitModel',
    'EditProductUnitModel',
    'DeleteProductUnitModel',
    'ProductCategoryModel',
    'ProductCategoryTreeModel',
    'ProductCategoryQueryModel',
    'ProductCategoryPageQueryModel',
    'AddProductCategoryModel',
    'EditProductCategoryModel',
    'DeleteProductCategoryModel',
    'ProductBrandModel',
    'ProductBrandQueryModel',
    'ProductBrandPageQueryModel',
    'AddProductBrandModel',
    'EditProductBrandModel',
    'DeleteProductBrandModel'
]