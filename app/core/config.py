from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None

    # Database Configuration 
    DATABASE_URL: str
    SKIP_DB_INIT: bool = False  # Set to True to skip database initialization on startup
    
    # App Configuration 
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()


     
    
    

