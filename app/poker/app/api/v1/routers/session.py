from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import DeckModel, GameModel, RoundModel
from schemas import SessionSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/session",
    response_model=SessionSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_session(
    api_token: str = Query(...),
    deck_id: int = Query(...),
    game_id: int = Query(...),
    round_id: int = Query(...),
    session: AsyncSession = Depends(depends.get_session),
) -> SessionSchema:
    deck = await tools.store.deck_accessor.get_deck_by(
        session=session, where=(DeckModel.id == deck_id)
    )
    game = await tools.store.game_accessor.get_game_by(
        session=session, where=(GameModel.id == game_id)
    )
    round = await tools.store.game_round_accessor.get_round_by(
        session=session, where=(RoundModel.id == round_id)
    )

    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_session_accessor.create_session(
            session=nested_session.session,
            deck=deck,
            game=game,
            round=round,
        )

    return to_return
