from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from schemas import RoundSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/round",
    response_model=RoundSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_round(
    api_token: str = Query(...), session: AsyncSession = Depends(depends.get_session)
) -> RoundSchema:
    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_round_accessor.create_round(
            session=nested_session.session
        )

    return to_return
