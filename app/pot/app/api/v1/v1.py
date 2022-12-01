from fastapi import APIRouter

from .routers.pot import router as pot_router

router = APIRouter()
router.include_router(pot_router)
