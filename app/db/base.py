from app.db.session import Base, engine

# Import all models here so they are registered with SQLAlchemy
from app.models.user import User  # Import User model

async def init_db():
    """
    Initialize database - create all tables.
    Call this on application startup.
    """
    import asyncio
    try:
        # Try to connect with a timeout (5 seconds)
        await asyncio.wait_for(
            _create_tables(),
            timeout=5.0
        )
        print("✓ Database tables created successfully")
    except asyncio.TimeoutError:
        print("⚠ Warning: Database connection timeout (5s)")
        print("⚠ The application will start, but database operations may fail.")
        print("⚠ Please check your DATABASE_URL in .env file and ensure the database is accessible.")
    except Exception as e:
        error_msg = str(e)
        print(f"⚠ Warning: Could not initialize database")
        print(f"⚠ Error: {error_msg[:200]}...")  # Truncate long error messages
        print("⚠ The application will start, but database operations may fail.")
        print("⚠ Please check your DATABASE_URL in .env file and ensure the database is accessible.")
        # Don't raise - allow app to start even if DB is unavailable


async def _create_tables():
    """Helper function to create tables."""
    async with engine.begin() as conn:
        # This will create all tables defined in your models
        await conn.run_sync(Base.metadata.create_all)