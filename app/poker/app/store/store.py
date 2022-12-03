from handlers import setup_handlers

from .aiohttp_session.accessor import SessionAccessor
from .game import (
    CardAccessor,
    DeckAccessor,
    GameAccessor,
    GamePlayerAccessor,
    GameRoundAccessor,
    GameSessionAccessor,
    GameUserAccessor,
    LogicDeckAccessor,
)
from .integration import IntegrationUserAccessor
from .ws.accessor import WSAccessor


class Store:
    def __init__(self) -> None:
        self.aiohttp_accessor = SessionAccessor(self)
        self.card_accessor = CardAccessor(self)
        self.deck_accessor = DeckAccessor(self)
        self.game_accessor = GameAccessor(self)
        self.game_player_accessor = GamePlayerAccessor(self)
        self.game_round_accessor = GameRoundAccessor(self)
        self.game_session_accessor = GameSessionAccessor(self)
        self.game_user_accessor = GameUserAccessor(self)
        self.logic_deck_accessor = LogicDeckAccessor(self)
        self.integration_user_accessor = IntegrationUserAccessor(self)
        self.ws_accessor = WSAccessor(self)

    async def connect(self) -> None:
        await setup_handlers()
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
