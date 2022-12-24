from __future__ import annotations

from typing import Any, Awaitable, Callable, TypeVar

from pydantic import BaseModel

LikeAsyncCallbackType = TypeVar(
    "LikeAsyncCallbackType", bound=Callable[[BaseModel], Awaitable[Any]]
)
