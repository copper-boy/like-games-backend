from functools import wraps

from fastapi import HTTPException

from core.config import get_admin_settings


def admin_required(target: str) -> callable:
    def wrapper(function: callable) -> callable:
        @wraps(function)
        async def wrapped(*args: object, **kwargs: object) -> object:
            if kwargs.get(target) != get_admin_settings().ADMIN_INFINITY_ACCESS_TOKEN:
                raise HTTPException(
                    status_code=403,
                    detail="not a valid access token",
                )

            return await function(*args, **kwargs)

        return wrapped

    return wrapper
