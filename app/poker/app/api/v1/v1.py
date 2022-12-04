from fastapi import APIRouter

from .routers.deck import router as deck_router
from .routers.game import router as game_router
from .routers.round import router as round_router
from .routers.session import router as session_router
from .routers.user import router as user_router

router = APIRouter()
router.include_router(deck_router)
router.include_router(game_router)
router.include_router(round_router)
router.include_router(session_router)
router.include_router(user_router)
