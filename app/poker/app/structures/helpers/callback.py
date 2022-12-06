from typing import Any, Callable, TypeVar

CallbackType = TypeVar("CallbackType", bound=Callable[..., Any])
