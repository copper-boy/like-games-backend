from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from store import Store


class BaseAccessor:
    def __init__(self, store: "Store") -> None:
        self.store = store
