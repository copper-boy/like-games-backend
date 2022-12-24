from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Dict, Generic, List, Tuple, TypeVar

from ...schema import LikeEventSchema
from ..handler import LikeHandlerObject
from ..response import LikeTriggerResponseNamedTuple

LikeAsyncCallbackType = TypeVar("LikeAsyncCallbackType")


class LikeBaseEventObserver(ABC, Generic[LikeAsyncCallbackType]):
    def __init__(self) -> None:
        self.handlers: List[LikeHandlerObject] = []

    @abstractmethod
    def register(
        self, callback: LikeAsyncCallbackType, *filters: Tuple[LikeAsyncCallbackType]
    ) -> LikeAsyncCallbackType:  # pragma: no cover
        ...

    @abstractmethod
    async def trigger(
        self, event: LikeEventSchema, **kwargs: Dict
    ) -> LikeTriggerResponseNamedTuple:  # pragma: no cover
        ...

    def __call__(
        self,
        *filters: LikeAsyncCallbackType,
    ) -> Callable[[LikeAsyncCallbackType], LikeAsyncCallbackType]:
        def wrapper(callback: LikeAsyncCallbackType) -> LikeAsyncCallbackType:
            self.register(callback, *filters)
            return callback

        return wrapper
