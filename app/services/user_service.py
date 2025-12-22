from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from typing import Optional, List, Sequence
from icecream import ic

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def list_users(self) -> List[User]:
        """
        Get all users from database.
        """
        result = await self.db.execute(select(User)) 
        users = result.scalars().all()
        return list(users)  # Convert Sequence to List
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a specific user by ID.
        """
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email address.
        """
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return user
    
    async def create_user(self, email: str, username: str, hashed_password: str) -> User:
        """
        Create a new user.
        """
        db_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user