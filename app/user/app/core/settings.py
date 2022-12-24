from __future__ import annotations

from pydantic import BaseModel

from .config import get_jwt_settings


class Settings(BaseModel):
    authjwt_secret_key: str = get_jwt_settings().SECRET_KEY
    authjwt_algorithm: str = get_jwt_settings().ALGORITHM

    authjwt_token_location: set = {"cookies"}

    authjwt_cookie_csrf_protect: bool = False  # production ready
