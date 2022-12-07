from fastapi.requests import Request
from fastapi.websockets import WebSocket

from core.config import get_site_settings
from schemas import IntegrationUserSchema
from store.base import BaseAccessor


class UserAccessor(BaseAccessor):
    async def get_user_request(self, request: Request) -> IntegrationUserSchema:
        base_url = get_site_settings().AUTH_SITE_BASE_URL
        async with self.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.user/cookie/current",
            cookies=request.cookies,
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return IntegrationUserSchema.parse_obj(json)

    async def get_user_websocket(self, websocket: WebSocket) -> IntegrationUserSchema:
        base_url = get_site_settings().AUTH_SITE_BASE_URL
        async with self.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.user/cookie/current",
            cookies=websocket.cookies,
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return IntegrationUserSchema.parse_obj(json)
