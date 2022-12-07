from .aiohttp_session.accessor import SessionAccessor
from .integration import IntegrationUserAccessor
from .pot.accessor import PotAccessor
from .user.accessor import UserAccessor


class Store:
    def __init__(self) -> None:
        self.aiohttp_accessor = SessionAccessor(self)
        self.integration_user_accessor = IntegrationUserAccessor(self)
        self.pot_accessor = PotAccessor(self)
        self.user_accessor = UserAccessor(self)

    async def connect(self) -> None:
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
