from aiohttp import ClientSession
from loguru import logger

from store.base import BaseAccessor


class SessionAccessor(BaseAccessor):
    session: ClientSession = None

    async def connect(self) -> None:
        self.session = ClientSession()

    @logger.catch(exception=AttributeError)
    async def disconnect(self) -> None:
        await self.session.close()
