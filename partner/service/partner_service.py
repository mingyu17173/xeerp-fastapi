from sqlalchemy.ext.asyncio import AsyncSession
from dao.partner_dao import PartnerDao
from schemas.partner import PartnerModel, AddPartnerModel, EditPartnerModel, PartnerPageQueryModel
from schemas.partner import PartnerModel as PartnerSchema
from core.response import ResponseModel, PageResponseModel
from core.exceptions import PartnerNotFoundError, PartnerCodeExistsError

class PartnerService:
    @classmethod
    async def get_partner_detail(cls, db: AsyncSession, partner_id: int) -> ResponseModel:
        partner = await PartnerDao.get_partner_by_id(db, partner_id)
        if not partner:
            raise PartnerNotFoundError()
        
        data = PartnerSchema.from_orm(partner)
        return ResponseModel.success(data=data)

    @classmethod
    async def get_partner_list(cls, db: AsyncSession, query: PartnerPageQueryModel) -> PageResponseModel:
        rows = await PartnerDao.get_partner_list(db, query)
        total = await PartnerDao.get_partner_count(db, query)
        
        data = [PartnerSchema.from_orm(row) for row in rows]
        return PageResponseModel.success(rows=data, total=total, page_num=query.page_num, page_size=query.page_size)

    @classmethod
    async def get_customers(cls, db: AsyncSession) -> ResponseModel:
        partners = await PartnerDao.get_customers(db)
        data = [PartnerSchema.from_orm(p) for p in partners]
        return ResponseModel.success(data=data)

    @classmethod
    async def get_suppliers(cls, db: AsyncSession) -> ResponseModel:
        partners = await PartnerDao.get_suppliers(db)
        data = [PartnerSchema.from_orm(p) for p in partners]
        return ResponseModel.success(data=data)

    @classmethod
    async def add_partner(cls, db: AsyncSession, add_model: AddPartnerModel, create_user: str) -> ResponseModel:
        existing = await PartnerDao.get_partner_by_code(db, add_model.partner_code)
        if existing:
            raise PartnerCodeExistsError()
        
        partner = await PartnerDao.add_partner(db, add_model, create_user)
        await db.commit()
        
        data = PartnerSchema.from_orm(partner)
        return ResponseModel.success(data=data, message='添加成功')

    @classmethod
    async def edit_partner(cls, db: AsyncSession, edit_model: EditPartnerModel, update_user: str) -> ResponseModel:
        partner = await PartnerDao.get_partner_by_id(db, edit_model.partner_id)
        if not partner:
            raise PartnerNotFoundError()
        
        await PartnerDao.update_partner(db, edit_model, update_user)
        await db.commit()
        
        return ResponseModel.success(message='修改成功')

    @classmethod
    async def delete_partner(cls, db: AsyncSession, partner_id: int, update_user: str) -> ResponseModel:
        partner = await PartnerDao.get_partner_by_id(db, partner_id)
        if not partner:
            raise PartnerNotFoundError()
        
        await PartnerDao.delete_partner(db, partner_id, update_user)
        await db.commit()
        
        return ResponseModel.success(message='删除成功')