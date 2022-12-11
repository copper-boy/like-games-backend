from core.config import get_site_settings
from schemas import IntegrationLikeEvaluatorRequestSchema, IntegrationLikeEvaluatorResponseSchema
from store.base import BaseAccessor


class LikeAccessor(BaseAccessor):
    async def find_winners(
        self,
        json: IntegrationLikeEvaluatorRequestSchema,
    ) -> IntegrationLikeEvaluatorResponseSchema:
        base_url = get_site_settings().LIKE_SITE_BASE_URL
        async with self.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.like/kind/holdem/evaluator",
            json=json.dict(),
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return IntegrationLikeEvaluatorResponseSchema.parse_obj(json)
