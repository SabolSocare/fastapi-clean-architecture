from fastapi import APIRouter
from app.api.v1.user import router as user_router

router = APIRouter()

# Include all route modules here
router.include_router(user_router, tags=["users"])