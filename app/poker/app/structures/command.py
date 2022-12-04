from .hash import HashSupport
from .loader import LoaderHelper


class Command(HashSupport, LoaderHelper):
    def __init__(self, command: str, description: str = None) -> None:
        self.command = command
        self.description = description

    def __repr__(self) -> str:
        return f"Command<command={self.command}, description={self.description}>"

    def to_hash(self) -> str:
        return self.command

    def to_dict(self) -> dict:
        return {"command": self.command, "description": self.description}
