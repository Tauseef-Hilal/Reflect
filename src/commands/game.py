import asyncio
from datetime import (
    datetime,
    timedelta
)

from discord import (
    Cog,
    SlashCommandGroup,
    ApplicationContext
)

from ..bot import ICodeBot

GAME_COMMANDS = SlashCommandGroup("game", "Game commands")

class GameCommands(Cog):
    """
    Game commands
    """
    
    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize
        """
        
        super().__init__()
        self._bot = bot
    
    @GAME_COMMANDS.command(name="tictactoe")
    async def _ttt(self, ctx: ApplicationContext) -> None:
        # TODO
        pass