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
from .integration import IntegrationLikeAccessor, IntegrationPotAccessor, IntegrationUserAccessor


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
        self.integration_like_accessor = IntegrationLikeAccessor(self)
        self.integration_pot_accessor = IntegrationPotAccessor(self)
        self.integration_user_accessor = IntegrationUserAccessor(self)

    async def connect(self) -> None:
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
