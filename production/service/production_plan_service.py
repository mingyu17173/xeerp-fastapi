from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from dao.production_plan_dao import ProductionPlanDao
from models.production_plan import SysProductionPlan
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.production_plan_schema import ProductionPlanModel, AddProductionPlanModel, EditProductionPlanModel, ProductionPlanPageQueryModel

class ProductionPlanService:
    @classmethod
    async def get_plan_detail(cls, db: AsyncSession, plan_id: int) -> Optional[ProductionPlanModel]:
        plan = await ProductionPlanDao.get_plan_by_id(db, plan_id)
        if plan:
            return ProductionPlanModel.model_validate(plan)
        return None

    @classmethod
    async def get_plan_list(cls, db: AsyncSession, query_model: ProductionPlanPageQueryModel) -> PageResponseModel:
        plans, total = await ProductionPlanDao.get_plan_list(db, query_model)
        plan_models = [ProductionPlanModel.model_validate(p) for p in plans]
        return PageResponseModel(
            rows=plan_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_plan(cls, request: Request, db: AsyncSession, add_model: AddProductionPlanModel) -> CrudResponseModel:
        if await ProductionPlanDao.get_plan_by_code(db, add_model.plan_code):
            return CrudResponseModel(is_success=False, message=f"生产计划编号 '{add_model.plan_code}' 已存在")

        plan = SysProductionPlan(
            plan_code=add_model.plan_code,
            product_id=add_model.product_id,
            product_name=add_model.product_name,
            bom_id=add_model.bom_id,
            plan_quantity=add_model.plan_quantity,
            warehouse_id=add_model.warehouse_id,
            start_date=add_model.start_date,
            end_date=add_model.end_date,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        await ProductionPlanDao.add_plan(db, plan)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_plan(cls, request: Request, db: AsyncSession, edit_model: EditProductionPlanModel) -> CrudResponseModel:
        existing = await ProductionPlanDao.get_plan_by_id(db, edit_model.plan_id)
        if not existing:
            return CrudResponseModel(is_success=False, message='生产计划不存在')

        code_exists = await ProductionPlanDao.get_plan_by_code(db, edit_model.plan_code)
        if code_exists and code_exists.plan_id != edit_model.plan_id:
            return CrudResponseModel(is_success=False, message=f"生产计划编号 '{edit_model.plan_code}' 已存在")

        plan = SysProductionPlan(
            plan_id=edit_model.plan_id,
            plan_code=edit_model.plan_code,
            product_id=edit_model.product_id,
            product_name=edit_model.product_name,
            bom_id=edit_model.bom_id,
            plan_quantity=edit_model.plan_quantity,
            warehouse_id=edit_model.warehouse_id,
            start_date=edit_model.start_date,
            end_date=edit_model.end_date,
            remark=edit_model.remark,
            update_by=getattr(request.state, 'user_name', 'system'),
            update_time=datetime.now()
        )

        result = await ProductionPlanDao.update_plan(db, plan)
        await db.commit()

        return CrudResponseModel(is_success=True, message='修改成功') if result > 0 else CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def start_production(cls, request: Request, db: AsyncSession, plan_id: int) -> CrudResponseModel:
        plan = await ProductionPlanDao.get_plan_by_id(db, plan_id)
        if not plan:
            return CrudResponseModel(is_success=False, message='生产计划不存在')

        if plan.status != '0':
            return CrudResponseModel(is_success=False, message='只能启动待生产状态的计划')

        plan.status = '1'
        plan.update_by = getattr(request.state, 'user_name', 'system')
        plan.update_time = datetime.now()

        await ProductionPlanDao.update_plan(db, plan)
        await db.commit()
        return CrudResponseModel(is_success=True, message='已开始生产')