from __future__ import annotations

from functools import wraps
from typing import Any, Callable
from fastapi import HTTPException

from core.config import get_admin_settings


def admin_required(target: str) -> Callable[..., Any]:
    def wrapper(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        async def wrapped(*args: tuple, **kwargs: dict) -> Any:
            if kwargs.get(target) != get_admin_settings().ADMIN_INFINITY_ACCESS_TOKEN:
                raise HTTPException(status_code=403, detail="not a valid access token")

            return await function(*args, **kwargs)

        return wrapped

    return wrapper
