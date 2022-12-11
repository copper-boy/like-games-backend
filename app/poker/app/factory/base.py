from abc import ABC, abstractmethod


class BaseFactory(ABC):
    @abstractmethod
    def build(self, *args: tuple, **kwargs: dict) -> ...:  # pragma: no cover
        ...
