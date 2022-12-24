from __future__ import annotations

from typing import Dict, Tuple

from ...likeenums import LikeTriggerResultEnum
from ...schema import LikeEventSchema
from ..filter import LikeFilterObject
from ..handler import LikeHandlerObject
from ..response import LikeTriggerResponseNamedTuple
from .base import LikeAsyncCallbackType, LikeBaseEventObserver


class LikeEventObserver(LikeBaseEventObserver[LikeAsyncCallbackType]):
    def __init__(self) -> None:
        super(LikeEventObserver, self).__init__()

    def register(
        self, callback: LikeAsyncCallbackType, *filters: Tuple[LikeAsyncCallbackType]
    ) -> LikeAsyncCallbackType:
        self.handlers.append(
            LikeHandlerObject(callback=callback, filters=[LikeFilterObject(f) for f in filters])
        )

        return callback

    async def trigger(
        self, event: LikeEventSchema, **kwargs: Dict
    ) -> LikeTriggerResponseNamedTuple:
        for handler in self.handlers:
            result, data = await handler.check(event, **kwargs)

            if result:
                kwargs.update(data, handler=handler)
                return LikeTriggerResponseNamedTuple(
                    handling=LikeTriggerResultEnum.SUCCESSFULLY,
                    result=await handler.call(event, **kwargs),
                )

        return LikeTriggerResponseNamedTuple(handling=LikeTriggerResultEnum.UNHANDLED, result=None)
