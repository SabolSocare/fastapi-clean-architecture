from fastapi import APIRouter
from app.api.v1.user import router as user_router
from app.api.v1.student import router as student_router

router = APIRouter()

# Include all route modules here
router.include_router(user_router, tags=["users"])
router.include_router(student_router, tags=["students"])