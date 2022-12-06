from dataclasses import dataclass

from .mixins import AsyncCallableMixin


@dataclass
class HandlerObject(AsyncCallableMixin):
    to_filter: str

    def check(self, to_filter: str) -> bool:
        return self.to_filter == to_filter
