from __future__ import annotations

from typing import Dict, List

from ..exceptions import (
    LikeRouterObserverAlreadyRegisteredError,
    LikeRouterObserverNotRegisteredError,
    LikeRouterRegisterError,
)
from ..likeenums import LikeTriggerResultEnum
from ..liketypes import LikeAllowAttributesMixin, LikeEventObserver, LikeTriggerResponseNamedTuple
from ..schema import LikeEventSchema


class LikeRouter(LikeAllowAttributesMixin):
    def __init__(self) -> None:
        self.included_routers: List[LikeRouter] = []

        self.observers: Dict[str, LikeEventObserver] = {}

    def register(self, name: str, observer: LikeEventObserver) -> None:
        exists = self.observers.get(name)
        if exists:
            raise LikeRouterObserverAlreadyRegisteredError(f"observer with {name} already exists")
        if not name.startswith("like"):
            raise LikeRouterRegisterError(f"observer name must starts with `like`, got {name}")

        self.observers[name] = observer

    def include_router(self, router: LikeRouter) -> None:
        self.included_routers.append(router)

    async def event(
        self, update_type: str, event: LikeEventSchema, **kwargs: Dict
    ) -> LikeTriggerResponseNamedTuple:
        observer = self.observers.get(update_type)
        if not observer:
            raise LikeRouterObserverNotRegisteredError(
                f"observer with {update_type} doesn't exists"
            )

        return await self._event(observer=observer, update_type=update_type, event=event, **kwargs)

    async def _event(
        self, observer: LikeEventObserver, update_type: str, event: LikeEventSchema, **kwargs: Dict
    ) -> LikeTriggerResponseNamedTuple:
        response = await observer.trigger(event=event, **kwargs)
        if response.handling == LikeTriggerResultEnum.SUCCESSFULLY:
            return response
        for router in self.included_routers:
            response = await router.event(update_type=update_type, event=event, **kwargs)
            if response.handling == LikeTriggerResultEnum.SUCCESSFULLY:
                return response

        return response
