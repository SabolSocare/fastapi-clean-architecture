from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_service import UserService


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """
    Dependency function that provides UserService instance.
    """
    return UserService(db)

