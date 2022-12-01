from fastapi.requests import Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqladmin.authentication import AuthenticationBackend

from core.config import get_admin_settings

from .token import create_token


class Backend(AuthenticationBackend):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(Backend, self).__init__(*args, **kwargs)

    async def login(self, request: Request) -> bool:
        authorize = AuthJWT()

        form = await request.form()
        username, password = form.get("username"), form.get("password")
        _config = get_admin_settings()

        if username == _config.ADMIN_LOGIN and password == _config.ADMIN_PASSWORD:
            token = create_token(authorize=authorize, subject=_config.ADMIN_WORD)
            request.session.update({"token": token})

            return True

        return False

    async def logout(self, request: Request) -> bool:
        authorize = AuthJWT()

        token = request.session.get("token")

        if not token:
            return False

        try:
            _config = get_admin_settings()
            subject = authorize.get_raw_jwt(token)

            if subject != _config.ADMIN_WORD:
                return False
        except AuthJWTException:
            return False

        request.session.clear()

        return True

    async def authenticate(self, request: Request) -> bool:
        authorize = AuthJWT()

        token = request.session.get("token")

        if not token:
            return False

        try:
            _config = get_admin_settings()
            subject = authorize.get_raw_jwt(token)

            if subject != _config.ADMIN_WORD:
                return False
        except AuthJWTException:
            return False
        else:
            return True
