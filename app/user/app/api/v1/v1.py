from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import UserModel
from schemas.user import UserRegistrationSchema, UserSchema
from utils import auth, helpers

from .routers.cookie import router as cookie_router
from .routers.telegram import router as telegram_router

router = APIRouter()
router.include_router(cookie_router)
router.include_router(telegram_router)


@router.post(
    path="/registration",
    response_description="The user on successful registration",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    user_data: UserRegistrationSchema, session: AsyncSession = Depends(depends.get_session)
) -> UserSchema:

    user = await tools.store.user_accessor.get_user_by(
        session=session, where=(UserModel.email == user_data.email)
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with {user.email=} already exits",
        )

    password_len = len(user_data.password)

    if password_len < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"password length must be greater than 8, got {password_len=}",
        )
    hashed_password = auth.get_password_hash(user_data.password)

    user = await helpers.create_new_user(
        session=session,
        hashed_password=hashed_password,
        email=user_data.email,
        username=user_data.username,
    )

    return user
