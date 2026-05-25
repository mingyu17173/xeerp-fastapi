# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: partner_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from models.partner import SysPartner, PartnerType, PartnerStatus
from schemas.partner import AddPartnerModel, EditPartnerModel
from typing import Optional, List

class PartnerDao:
    @classmethod
    async def get_partner_by_id(cls, db: AsyncSession, partner_id: int) -> Optional[SysPartner]:
        result = await db.execute(select(SysPartner).where(
            SysPartner.partner_id == partner_id,
            SysPartner.is_delete == False
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_partner_by_code(cls, db: AsyncSession, partner_code: str) -> Optional[SysPartner]:
        result = await db.execute(select(SysPartner).where(
            SysPartner.partner_code == partner_code,
            SysPartner.is_delete == False
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_partner_list(cls, db: AsyncSession, query) -> List[SysPartner]:
        stmt = select(SysPartner).where(SysPartner.is_delete == False)
        
        if query.partner_code:
            stmt = stmt.filter(SysPartner.partner_code.like(f'%{query.partner_code}%'))
        if query.partner_name:
            stmt = stmt.filter(SysPartner.partner_name.like(f'%{query.partner_name}%'))
        if query.partner_type:
            stmt = stmt.filter(SysPartner.partner_type == query.partner_type)
        if query.status:
            stmt = stmt.filter(SysPartner.status == query.status)
        
        stmt = stmt.order_by(SysPartner.create_time.desc())
        
        offset = (query.page_num - 1) * query.page_size
        stmt = stmt.offset(offset).limit(query.page_size)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_partner_count(cls, db: AsyncSession, query) -> int:
        stmt = select(func.count(SysPartner.partner_id)).where(SysPartner.is_delete == False)
        
        if query.partner_code:
            stmt = stmt.filter(SysPartner.partner_code.like(f'%{query.partner_code}%'))
        if query.partner_name:
            stmt = stmt.filter(SysPartner.partner_name.like(f'%{query.partner_name}%'))
        if query.partner_type:
            stmt = stmt.filter(SysPartner.partner_type == query.partner_type)
        if query.status:
            stmt = stmt.filter(SysPartner.status == query.status)
        
        result = await db.execute(stmt)
        return result.scalar_one()

    @classmethod
    async def get_customers(cls, db: AsyncSession) -> List[SysPartner]:
        stmt = select(SysPartner).where(
            SysPartner.is_delete == False,
            SysPartner.status == PartnerStatus.ACTIVE,
            (SysPartner.partner_type == PartnerType.CUSTOMER) | (SysPartner.partner_type == PartnerType.BOTH)
        ).order_by(SysPartner.partner_name)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_suppliers(cls, db: AsyncSession) -> List[SysPartner]:
        stmt = select(SysPartner).where(
            SysPartner.is_delete == False,
            SysPartner.status == PartnerStatus.ACTIVE,
            (SysPartner.partner_type == PartnerType.SUPPLIER) | (SysPartner.partner_type == PartnerType.BOTH)
        ).order_by(SysPartner.partner_name)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def add_partner(cls, db: AsyncSession, add_model: AddPartnerModel, create_user: str):
        partner = SysPartner(
            partner_code=add_model.partner_code,
            partner_name=add_model.partner_name,
            short_name=add_model.short_name,
            partner_type=add_model.partner_type,
            contact_person=add_model.contact_person,
            phone=add_model.phone,
            mobile=add_model.mobile,
            email=add_model.email,
            address=add_model.address,
            province=add_model.province,
            city=add_model.city,
            district=add_model.district,
            tax_no=add_model.tax_no,
            bank_name=add_model.bank_name,
            bank_account=add_model.bank_account,
            credit_limit=add_model.credit_limit,
            credit_days=add_model.credit_days,
            remark=add_model.remark,
            create_user=create_user
        )
        db.add(partner)
        await db.flush()
        return partner

    @classmethod
    async def update_partner(cls, db: AsyncSession, edit_model: EditPartnerModel, update_user: str):
        stmt = update(SysPartner).where(SysPartner.partner_id == edit_model.partner_id).values(
            partner_name=edit_model.partner_name,
            short_name=edit_model.short_name,
            partner_type=edit_model.partner_type,
            status=edit_model.status,
            contact_person=edit_model.contact_person,
            phone=edit_model.phone,
            mobile=edit_model.mobile,
            email=edit_model.email,
            address=edit_model.address,
            province=edit_model.province,
            city=edit_model.city,
            district=edit_model.district,
            tax_no=edit_model.tax_no,
            bank_name=edit_model.bank_name,
            bank_account=edit_model.bank_account,
            credit_limit=edit_model.credit_limit,
            credit_days=edit_model.credit_days,
            remark=edit_model.remark,
            update_user=update_user
        )
        await db.execute(stmt)

    @classmethod
    async def delete_partner(cls, db: AsyncSession, partner_id: int, update_user: str):
        stmt = update(SysPartner).where(SysPartner.partner_id == partner_id).values(
            is_delete=True,
            update_user=update_user
        )
        await db.execute(stmt)