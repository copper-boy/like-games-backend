from __future__ import annotations

from asyncio import get_event_loop
from contextvars import copy_context
from dataclasses import dataclass, field
from functools import partial
from inspect import FullArgSpec, getfullargspec, isawaitable, iscoroutinefunction
from typing import Any, Dict, Tuple

from likeevents.liketypes.callback import LikeAsyncCallbackType


@dataclass
class LikeAsyncCallableMixin:
    callback: LikeAsyncCallbackType
    awaitable: bool = field(init=False)
    spec: FullArgSpec = field(init=False)

    def __post_init__(self) -> None:
        self.awaitable = isawaitable(self.callback) or iscoroutinefunction(self.callback)
        self.spec = getfullargspec(self.callback)

    def _prepare_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if self.spec.varkw:
            return kwargs

        return {
            k: v for k, v in kwargs.items() if k in self.spec.args or k in self.spec.kwonlyargs
        }

    async def call(self, *args: Tuple, **kwargs: Dict) -> Any:
        prepared_kwargs = self._prepare_kwargs(kwargs)
        wrapped = partial(self.callback, *args, **prepared_kwargs)
        if self.awaitable:
            return await wrapped()

        loop = get_event_loop()
        context = copy_context()
        wrapped = partial(context.run, wrapped)
        return await loop.run_in_executor(None, wrapped)


class LikeAllowAttributesMixin:
    def __getattribute__(self, name: str) -> Any:
        if name.startswith("like"):
            return self.observers.get(name)
        return super(LikeAllowAttributesMixin, self).__getattribute__(name)
