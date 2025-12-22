from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.api.v1.dependencies import get_user_service

router = APIRouter()


@router.get("/users", response_model=list[UserRead])
async def get_users(service: UserService = Depends(get_user_service)):
    """
    Get all users from database.
    """
    return await service.list_users()


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """
    Get a specific user by ID.
    """
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """
    Create a new user.
    """
    # Check if user already exists
    existing_user = await service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user (in real app, hash the password)
    db_user = await service.create_user(
        email=user.email,
        username=user.username,
        hashed_password=user.password  # Should hash this in production
    )
    return db_user