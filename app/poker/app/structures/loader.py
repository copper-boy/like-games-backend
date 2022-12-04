from abc import ABC, abstractmethod
from typing import Type


class LoaderHelper(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        ...


class Loader:
    def load_to_dict(
        self,
        obj: Type[LoaderHelper],
        include: set[str] = None,
        exclude: set[str] = None,
    ) -> dict:
        generated = obj.to_dict()
        if not include:
            include = set(generated.keys())
        if not exclude:
            exclude = set()

        to_return: dict = {}
        for k, v in generated.items():
            if k in include and k not in exclude:
                to_return[k] = v

        return to_return
