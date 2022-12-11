from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from schemas import DeckSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/deck",
    response_model=DeckSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_deck(
    api_token: str = Query(...),
    session: AsyncSession = Depends(depends.get_session),
) -> DeckSchema:
    """
    Creates the deck in database

    :param api_token:
      admin access token
    :param session:
      async database session
    :return:
      Created deck
    """

    async with session.begin_nested() as nested_session:
        to_return = await tools.store.deck_accessor.create_deck(session=nested_session.session)

    return to_return
