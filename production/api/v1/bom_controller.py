from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.get_db import get_db
from service.bom_service import BomService
from schemas.bom_schema import BomModel, AddBomModel, EditBomModel, BomPageQueryModel
from schemas.common_schema import CrudResponseModel, PageResponseModel

router = APIRouter(prefix='/bom', tags=['BOM管理'])

@router.get('/{bom_id}', response_model=BomModel)
async def get_bom_detail(bom_id: int, db: AsyncSession = Depends(get_db)):
    return await BomService.get_bom_detail(db, bom_id)

@router.get('/list', response_model=PageResponseModel[BomModel])
async def get_bom_list(query: BomPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await BomService.get_bom_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_bom(request: Request, add_model: AddBomModel, db: AsyncSession = Depends(get_db)):
    return await BomService.add_bom(request, db, add_model)

@router.put('', response_model=CrudResponseModel)
async def edit_bom(request: Request, edit_model: EditBomModel, db: AsyncSession = Depends(get_db)):
    return await BomService.edit_bom(request, db, edit_model)

@router.delete('/{bom_id}', response_model=CrudResponseModel)
async def delete_bom(request: Request, bom_id: int, db: AsyncSession = Depends(get_db)):
    return await BomService.delete_bom(request, db, bom_id)