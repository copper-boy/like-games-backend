from fastapi import APIRouter

from .v3 import router as v3_router

router = APIRouter()
router.include_router(v3_router)
