from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from models.approval import (
    SysApprovalFlow, SysApprovalNode, SysApprovalInstance, 
    SysApprovalRecord, ApprovalStatus, ApprovalNodeType
)
from schemas.approval import AddApprovalInstanceModel
from typing import Optional, List

class ApprovalDao:
    @classmethod
    async def get_flow_by_id(cls, db: AsyncSession, flow_id: int) -> Optional[SysApprovalFlow]:
        result = await db.execute(select(SysApprovalFlow).where(SysApprovalFlow.flow_id == flow_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_flow_list(cls, db: AsyncSession, approval_type: Optional[str] = None) -> List[SysApprovalFlow]:
        stmt = select(SysApprovalFlow).where(SysApprovalFlow.is_active == True)
        if approval_type:
            stmt = stmt.filter(SysApprovalFlow.approval_type == approval_type)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_nodes_by_flow(cls, db: AsyncSession, flow_id: int) -> List[SysApprovalNode]:
        stmt = select(SysApprovalNode).where(SysApprovalNode.flow_id == flow_id).order_by(SysApprovalNode.node_order)
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_instance_by_id(cls, db: AsyncSession, instance_id: int) -> Optional[SysApprovalInstance]:
        result = await db.execute(select(SysApprovalInstance).where(SysApprovalInstance.instance_id == instance_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_instance_by_source(cls, db: AsyncSession, source_type: str, source_id: int) -> Optional[SysApprovalInstance]:
        result = await db.execute(select(SysApprovalInstance).where(
            SysApprovalInstance.source_type == source_type,
            SysApprovalInstance.source_id == source_id
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_instance_list(cls, db: AsyncSession, user_id: Optional[str] = None) -> List[SysApprovalInstance]:
        stmt = select(SysApprovalInstance).order_by(SysApprovalInstance.submit_time.desc())
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def create_instance(cls, db: AsyncSession, add_model: AddApprovalInstanceModel, submit_user: str):
        instance = SysApprovalInstance(
            flow_id=add_model.flow_id,
            source_type=add_model.source_type,
            source_id=add_model.source_id,
            source_code=add_model.source_code,
            submit_user=submit_user,
            remark=add_model.remark
        )
        db.add(instance)
        await db.flush()
        
        nodes = await cls.get_nodes_by_flow(db, add_model.flow_id)
        first_node = next((n for n in nodes if n.node_type == ApprovalNodeType.APPROVE), None)
        if first_node:
            instance.current_node_id = first_node.node_id
            await db.flush()
        
        return instance

    @classmethod
    async def update_instance_status(cls, db: AsyncSession, instance_id: int, status: ApprovalStatus, finish_time=None):
        values = {'status': status}
        if finish_time:
            values['finish_time'] = finish_time
        stmt = update(SysApprovalInstance).where(SysApprovalInstance.instance_id == instance_id).values(values)
        await db.execute(stmt)

    @classmethod
    async def update_current_node(cls, db: AsyncSession, instance_id: int, node_id: int):
        stmt = update(SysApprovalInstance).where(SysApprovalInstance.instance_id == instance_id).values(current_node_id=node_id)
        await db.execute(stmt)

    @classmethod
    async def add_record(cls, db: AsyncSession, instance_id: int, node_id: int, status: ApprovalStatus, approver: str, comment: str):
        record = SysApprovalRecord(
            instance_id=instance_id,
            node_id=node_id,
            status=status,
            approver=approver,
            comment=comment
        )
        db.add(record)
        await db.flush()
        return record