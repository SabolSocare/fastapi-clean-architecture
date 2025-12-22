from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    """Schema for reading/returning user data."""
    id: int
    email: str
    username: str
    is_active: bool
    
    class Config:
        from_attributes = True

