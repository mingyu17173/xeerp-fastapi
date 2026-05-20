from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional


class ProductModel(BaseModel):
    """
    商品信息模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    product_id: Optional[int] = Field(default=None, description='商品ID')
    product_name: Optional[str] = Field(default=None, description='商品名称')
    product_code: Optional[str] = Field(default=None, description='商品编码')
    category_id: Optional[int] = Field(default=None, description='分类ID')
    brand_id: Optional[int] = Field(default=None, description='品牌ID')
    unit_id: Optional[int] = Field(default=None, description='单位ID')
    description: Optional[str] = Field(default=None, description='商品描述')
    price: Optional[Decimal] = Field(default=None, description='售价')
    cost_price: Optional[Decimal] = Field(default=None, description='成本价')
    stock: Optional[int] = Field(default=None, description='库存数量')
    status: Optional[str] = Field(default=None, description='状态（0正常 1停用）')
    is_delete: Optional[str] = Field(default=None, description='删除标志')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')


class ProductQueryModel(ProductModel):
    """
    商品查询模型
    """
    pass


class ProductPageQueryModel(ProductModel):
    """
    商品分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class AddProductModel(BaseModel):
    """
    新增商品模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    product_name: str = Field(description='商品名称')
    product_code: str = Field(description='商品编码')
    category_id: Optional[int] = Field(default=None, description='分类ID')
    brand_id: Optional[int] = Field(default=None, description='品牌ID')
    unit_id: Optional[int] = Field(default=None, description='单位ID')
    description: Optional[str] = Field(default=None, description='商品描述')
    price: Decimal = Field(default=Decimal('0.00'), description='售价')
    cost_price: Decimal = Field(default=Decimal('0.00'), description='成本价')
    stock: int = Field(default=0, description='库存数量')
    status: str = Field(default='0', description='状态（0正常 1停用）')
    remark: Optional[str] = Field(default=None, description='备注')


class EditProductModel(AddProductModel):
    """
    编辑商品模型
    """
    product_id: int = Field(description='商品ID')


class DeleteProductModel(BaseModel):
    """
    删除商品模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    product_ids: str = Field(description='需要删除的商品ID，多个用逗号分隔')