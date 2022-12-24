from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import UserModel
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
    """
    Creates user in database

    :param user:
      user object from user service
    :param session:
      async database session
    :return:
      created user
    """
    to_select = await tools.store.game_user_accessor.create_user(
        session=session,
        user_id=user.id,
    )

    return await tools.store.game_user_accessor.get_user_by(
        session=session, where=(UserModel.id == to_select.id)
    )
