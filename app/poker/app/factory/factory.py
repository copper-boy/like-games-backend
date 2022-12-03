from .connection.builder import ConnectionFactory


class Factory:
    def __init__(self) -> None:
        self.connection_factory = ConnectionFactory()
