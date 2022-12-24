from __future__ import annotations

from functools import wraps
from typing import Any, Callable

def login_required(target: str, attribute: str) -> Callable[..., Any]:
    def wrapper(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        async def wrapped(*args: tuple, **kwargs: dict) -> Any:
            kwargs.get(target).__getattribute__(attribute)()

            return await function(*args, **kwargs)

        return wrapped

    return wrapper
