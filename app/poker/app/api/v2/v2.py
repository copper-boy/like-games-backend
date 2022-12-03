from fastapi import APIRouter

from .routers.game import router as game_router
from .routers.round import router as round_router

router = APIRouter()
router.include_router(game_router)
router.include_router(round_router)
