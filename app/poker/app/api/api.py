from fastapi import APIRouter

from .v1 import router as v1_router
from .v2 import router as v2_router
from .v3 import router as v3_router
from .ws import router as ws_router


router = APIRouter()
router.include_router(v1_router)
router.include_router(v2_router)
router.include_router(v3_router)
router.include_router(ws_router)
