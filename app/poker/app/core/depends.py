from __future__ import annotations

from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_session(request: Request) -> AsyncSession:
    """
    Gets async database session from request

    :param request:
      request for endpoint
    :return:
      async database session
    """

    return request.state.session
