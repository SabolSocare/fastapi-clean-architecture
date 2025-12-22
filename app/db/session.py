from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from app.core.config import settings

# Ensure DATABASE_URL uses psycopg driver
database_url = settings.DATABASE_URL
if "postgresql://" in database_url and "+psycopg" not in database_url:
    # Replace postgresql:// with postgresql+psycopg://
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
elif "postgresql+asyncpg://" in database_url:
    # Replace asyncpg with psycopg
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)

# Create async engine with psycopg 
engine = create_async_engine(
    database_url,
    echo=True,    # Set to False in production
    future=True,  
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,       # Maximum number of connections to allow in excess of pool_size
)

# Create async session factory 
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class models for SQLAlchemy 
Base = declarative_base()

# Dependency to get database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields a database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

            