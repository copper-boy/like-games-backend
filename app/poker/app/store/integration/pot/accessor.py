from __future__ import annotations

from core.config import get_admin_settings, get_site_settings
from schemas import IntegrationPotSchema, IntegrationPotUpdateSchema
from store.base import BaseAccessor


class PotAccessor(BaseAccessor):
    async def get_pot(self, user_id: int) -> IntegrationPotSchema:
        base_url = get_site_settings().POT_SITE_BASE_URL
        async with self.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.pot/view/{user_id}",
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return IntegrationPotSchema.parse_obj(json)

    async def update_pot(
        self, user_id: int, json: IntegrationPotUpdateSchema
    ) -> IntegrationPotSchema:
        base_url = get_site_settings().POT_SITE_BASE_URL
        async with self.store.aiohttp_accessor.session.put(
            url=f"{base_url}/api.pot/update/{user_id}",
            json=json.dict(),
            params={"api_token": get_admin_settings().ADMIN_INFINITY_ACCESS_TOKEN},
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return IntegrationPotSchema.parse_obj(json)
