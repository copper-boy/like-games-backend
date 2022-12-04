from core import tools
from structures.command import Command

from .game import allin_handler, bet_handler, call_handler, check_handler, fold_handler, up_handler
from .helpers import (
    commands_handler,
    mecards_handler,
    playercards_handler,
    players_handler,
    tablecards_handler,
)


async def setup_handlers() -> None:
    tools.store.ws_accessor.register_handler(
        command=Command(command="allin", description="Release allin action"),
        function=allin_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="bet", description="Release bet action"),
        function=bet_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="call", description="Release call action"),
        function=call_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="check", description="Release check action"),
        function=check_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="fold", description="Release fold action"),
        function=fold_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="up", description="Release up action"),
        function=up_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="commands", description="The list of registered commands"),
        function=commands_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="mecards", description="The current player cards"),
        function=mecards_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="playercards", description="The cards of player"),
        function=playercards_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(
            command="players", description="The players in game with no current player"
        ),
        function=players_handler,
    )
    tools.store.ws_accessor.register_handler(
        command=Command(command="tablecards", description="The table cards"),
        function=tablecards_handler,
    )
