from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .filter import LikeFilterObject
from .mixins import LikeAsyncCallableMixin


@dataclass
class LikeHandlerObject(LikeAsyncCallableMixin):
    filters: Optional[List[LikeFilterObject]] = None

    async def check(self, *args: Tuple, **kwargs: Dict) -> Tuple[bool, Dict[str, Any]]:
        if not self.filters:
            return True, kwargs

        for event_filter in self.filters:
            check = await event_filter.call(*args, **kwargs)

            if not check:
                return False, kwargs
            if isinstance(check, Dict):
                kwargs.update(check)

        return True, kwargs
