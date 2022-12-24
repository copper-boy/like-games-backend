from __future__ import annotations

from typing import AsyncIterable, Dict

from ..liketypes import LikeEventObserver, LikeTriggerResponseNamedTuple
from ..schema import LikeEventSchema
from .router import LikeRouter


class LikeRootRouter(LikeRouter):
    def __init__(self) -> None:
        super(LikeRootRouter, self).__init__()

        self.register("like_update", LikeEventObserver())

    async def feed_update(
        self, update: LikeEventSchema, **kwargs: Dict
    ) -> LikeTriggerResponseNamedTuple:
        return await self.like_update.trigger(update, **kwargs)

    async def start_listen(
        self, updates_from: AsyncIterable[LikeEventSchema], **kwargs: Dict
    ) -> None:
        async for update in updates_from:
            await self.feed_update(update=update, **kwargs)
