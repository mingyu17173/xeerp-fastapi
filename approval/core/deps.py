from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import verify_jwt_token

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="未授权访问")
    
    try:
        token = token.replace("Bearer ", "")
        payload = verify_jwt_token(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

async def get_db_session(db: AsyncSession = Depends(get_db)):
    return db