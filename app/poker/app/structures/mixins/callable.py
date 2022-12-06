import inspect
from dataclasses import dataclass

from structures.helpers import CallbackType


@dataclass
class CallableMixin:
    callback: CallbackType


@dataclass
class AsyncCallableMixin(CallableMixin):
    @property
    def awaitable(self) -> bool:
        awaitable = inspect.isawaitable(self.callback) or inspect.iscoroutinefunction(
            self.callback
        )

        return awaitable
