# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: category_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from dao.category_dao import ProductCategoryDao
from models.category import SysProductCategory
from schemas.category_schema import (
    AddProductCategoryModel,
    DeleteProductCategoryModel,
    EditProductCategoryModel,
    ProductCategoryModel,
    ProductCategoryPageQueryModel,
    ProductCategoryTreeModel,
)
from schemas.common_schema import CrudResponseModel


class ProductCategoryService:
    """
    商品分类服务类
    """

    @classmethod
    async def get_category_detail_services(
        cls, db: AsyncSession, category_id: int
    ) -> Optional[ProductCategoryModel]:
        """
        获取分类详情
        """
        category = await ProductCategoryDao.get_category_by_id(db, category_id)
        if category:
            return ProductCategoryModel.model_validate(category)
        return None

    @classmethod
    async def get_category_list_services(
        cls, db: AsyncSession, query_model: ProductCategoryPageQueryModel
    ) -> Tuple[List[ProductCategoryModel], int]:
        """
        获取分类列表（分页）
        """
        categories, total = await ProductCategoryDao.get_category_list(db, query_model)
        category_models = [ProductCategoryModel.model_validate(category) for category in categories]
        return category_models, total

    @classmethod
    async def get_all_categories_services(cls, db: AsyncSession) -> List[ProductCategoryModel]:
        """
        获取所有启用的分类列表
        """
        categories = await ProductCategoryDao.get_all_categories(db)
        return [ProductCategoryModel.model_validate(category) for category in categories]

    @classmethod
    async def get_category_tree_services(cls, db: AsyncSession) -> List[ProductCategoryTreeModel]:
        """
        获取分类树形结构
        """
        all_categories = await ProductCategoryDao.get_all_categories(db)
        
        # 构建树形结构
        category_dict = {cat.category_id: cat for cat in all_categories}
        tree = []
        
        for category in all_categories:
            # 根节点（parent_id为None或0）
            if category.parent_id is None or category.parent_id == 0:
                tree.append(category)
            else:
                # 添加到父节点的children
                parent = category_dict.get(category.parent_id)
                if parent:
                    if not hasattr(parent, '_children'):
                        parent._children = []
                    parent._children.append(category)
        
        # 转换为树形模型
        def build_tree(node):
            model = ProductCategoryTreeModel.model_validate(node)
            if hasattr(node, '_children'):
                model.children = [build_tree(child) for child in node._children]
            return model
        
        return [build_tree(node) for node in tree]

    @classmethod
    async def add_category_services(
        cls, request: Request, db: AsyncSession, add_model: AddProductCategoryModel
    ) -> CrudResponseModel:
        """
        新增分类
        """
        if await ProductCategoryDao.check_category_code_exists(db, add_model.category_code):
            return CrudResponseModel(is_success=False, message=f"分类编码 '{add_model.category_code}' 已存在")

        # 如果是子分类，检查父分类是否存在
        if add_model.parent_id and add_model.parent_id != 0:
            parent_category = await ProductCategoryDao.get_category_by_id(db, add_model.parent_id)
            if not parent_category:
                return CrudResponseModel(is_success=False, message='父分类不存在')

        category = SysProductCategory(
            parent_id=add_model.parent_id if add_model.parent_id != 0 else None,
            category_name=add_model.category_name,
            category_code=add_model.category_code,
            sort_order=add_model.sort_order,
            status=add_model.status,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now(),
            remark=add_model.remark,
        )

        await ProductCategoryDao.add_category(db, category)
        await db.commit()

        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_category_services(
        cls, request: Request, db: AsyncSession, edit_model: EditProductCategoryModel
    ) -> CrudResponseModel:
        """
        编辑分类
        """
        existing_category = await ProductCategoryDao.get_category_by_id(db, edit_model.category_id)
        if not existing_category:
            return CrudResponseModel(is_success=False, message='分类不存在')

        if await ProductCategoryDao.check_category_code_exists(
            db, edit_model.category_code, exclude_id=edit_model.category_id
        ):
            return CrudResponseModel(is_success=False, message=f"分类编码 '{edit_model.category_code}' 已存在")

        # 如果是子分类，检查父分类是否存在
        if edit_model.parent_id and edit_model.parent_id != 0:
            parent_category = await ProductCategoryDao.get_category_by_id(db, edit_model.parent_id)
            if not parent_category:
                return CrudResponseModel(is_success=False, message='父分类不存在')

        # 不允许将自身作为父分类
        if edit_model.parent_id == edit_model.category_id:
            return CrudResponseModel(is_success=False, message='不能将自己设为父分类')

        category = SysProductCategory(
            category_id=edit_model.category_id,
            parent_id=edit_model.parent_id if edit_model.parent_id != 0 else None,
            category_name=edit_model.category_name,
            category_code=edit_model.category_code,
            sort_order=edit_model.sort_order,
            status=edit_model.status,
            update_by=getattr(request.state, 'user_name', 'system'),
            remark=edit_model.remark,
        )

        result = await ProductCategoryDao.update_category(db, category)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='修改成功')
        return CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def delete_category_services(
        cls, request: Request, db: AsyncSession, category_id: int
    ) -> CrudResponseModel:
        """
        删除分类
        """
        existing_category = await ProductCategoryDao.get_category_by_id(db, category_id)
        if not existing_category:
            return CrudResponseModel(is_success=False, message='分类不存在')

        # 检查是否有子分类
        if await ProductCategoryDao.has_children(db, category_id):
            return CrudResponseModel(is_success=False, message='该分类下有子分类，无法删除')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductCategoryDao.delete_category(db, category_id, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='删除成功')
        return CrudResponseModel(is_success=False, message='删除失败')

    @classmethod
    async def batch_delete_category_services(
        cls, request: Request, db: AsyncSession, delete_model: DeleteProductCategoryModel
    ) -> CrudResponseModel:
        """
        批量删除分类
        """
        try:
            category_ids = [int(id_str) for id_str in delete_model.category_ids.split(',') if id_str.strip()]
        except ValueError:
            return CrudResponseModel(is_success=False, message='分类ID格式错误')

        if not category_ids:
            return CrudResponseModel(is_success=False, message='请选择要删除的分类')

        # 检查是否有子分类
        for category_id in category_ids:
            if await ProductCategoryDao.has_children(db, category_id):
                return CrudResponseModel(is_success=False, message='存在包含子分类的分类，无法删除')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductCategoryDao.batch_delete_category(db, category_ids, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message=f'成功删除 {result} 条记录')
        return CrudResponseModel(is_success=False, message='删除失败')