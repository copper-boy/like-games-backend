from likeevents import LikeRouter

from .game import allin_router, bet_router, call_router, check_router, fold_router, up_router
from .helpers import (
    my_cards_router,
    player_cards_router,
    players_router,
    session_router,
    table_cards_router,
)

router = LikeRouter()
router.include_router(allin_router)
router.include_router(bet_router)
router.include_router(call_router)
router.include_router(check_router)
router.include_router(fold_router)
router.include_router(up_router)
router.include_router(my_cards_router)
router.include_router(player_cards_router)
router.include_router(players_router)
router.include_router(session_router)
router.include_router(table_cards_router)
