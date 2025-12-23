from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    """Schema for reading/returning user data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

