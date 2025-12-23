from app.db.session import Base, engine

# Import all models here so they are registered with SQLAlchemy
from app.models.user import User  # Import User model

async def init_db():
    """
    Initialize database - verify connection.
    
    Note: Database migrations should be run separately using Alembic:
    - Development: ./migrate.sh upgrade
    - Production: alembic upgrade head
    
    This function only verifies the database connection.
    """
    from app.core.config import settings
    
    # If SKIP_DB_INIT is True, skip database initialization
    if settings.SKIP_DB_INIT:
        print("⚠ Skipping database initialization (SKIP_DB_INIT=True)")
        print("⚠ Make sure to run migrations manually: alembic upgrade head")
        return
    
    try:
        # Just verify connection - migrations should be run separately
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✓ Database connection verified")
        print("ℹ Run migrations with: alembic upgrade head")
    except Exception as e:
        error_msg = str(e)
        print(f"⚠ Warning: Could not connect to database")
        print(f"⚠ Error: {error_msg[:200]}...")  # Truncate long error messages
        print("⚠ The application will start, but database operations may fail.")
        print("⚠ Please check your DATABASE_URL in .env file and ensure the database is accessible.")
        # Don't raise - allow app to start even if DB is unavailable