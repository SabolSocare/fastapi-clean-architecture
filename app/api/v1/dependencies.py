from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_service import UserService
from app.services.student_service import StudentService


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """
    Dependency function that provides UserService instance.
    """
    return UserService(db)


async def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    """
    Dependency function that provides StudentService instance.
    """
    return StudentService(db)

