from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from schemas import IntegrationUserSchema, UserSchema

router = APIRouter()


@router.post(
    path="/me",
    response_description="User model",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def me(
    user: IntegrationUserSchema = Depends(tools.store.integration_user_accessor.get_user_request),
    session: AsyncSession = Depends(depends.get_session),
) -> UserSchema:
    async with session.begin_nested() as nested_session:
        user = await tools.store.game_user_accessor.create_user(
            session=nested_session.session,
            user_id=user.id,
        )

    return user
