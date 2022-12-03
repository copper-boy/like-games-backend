from abc import ABC, abstractmethod


class BaseFactory(ABC):
    @abstractmethod
    def build(self, *args, **kwargs) -> ...:
        ...
