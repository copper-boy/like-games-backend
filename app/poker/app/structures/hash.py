from abc import abstractmethod


class HashSupport:
    def __hash__(self) -> int:
        to_hash = self.to_hash()

        return hash(to_hash)

    @abstractmethod
    def to_hash(self) -> str:
        ...
