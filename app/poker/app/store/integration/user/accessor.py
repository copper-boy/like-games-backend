from fastapi.requests import Request

from core.config import get_site_settings
from schemas.integration import IntegrationUserSchema
from store.base import BaseAccessor


class UserAccessor(BaseAccessor):
    async def get_user(self, request: Request) -> IntegrationUserSchema:
        base_url = get_site_settings().AUTH_SITE_BASE_URL
        async with self.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.user.cookie.current",
            cookies=request.cookies,
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return IntegrationUserSchema.parse_obj(json)
