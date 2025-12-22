from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import init_db
from app.api.v1 import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting application...")
    if not settings.SKIP_DB_INIT:
        await init_db()
    else:
        print("⚠ Skipping database initialization (SKIP_DB_INIT=True)")
    print("✓ Application startup complete")
    yield
    # Shutdown
    print("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "FastAPI Backend with Supabase"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint - checks if the application is running.
    """
    return {"status": "healthy", "message": "Application is running"}


@app.get("/health/db")
async def health_check_db():
    """
    Database health check endpoint - tests database connection.
    """
    from sqlalchemy import text
    from app.db.session import engine
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)