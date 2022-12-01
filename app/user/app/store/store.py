from .user.accessor import UserAccessor


class Store:
    def __init__(self) -> None:
        self.user_accessor = UserAccessor(self)

    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...
