import logging

from discord import Intents

from .bot import ICodeBot
from .commands.general import GeneralCommands
from .commands.moderation import ModerationCommands
from .commands.miscellaneous import MiscellaneousCommands
from .utils.env import (
    ICODE_GUILD_ID,
    BOT_TOKEN
)


def main() -> None:
    """
        Main
    """

    # Set Up Logging
    FORMAT = "[%(name)s] => [%(levelname)s] : %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    # Instantiate ICodeBot
    INTENTS = Intents.all()

    BOT = ICodeBot(
        description="The BOT made for iCODE Discord server.",
        intents=INTENTS,
        debug_guilds=[ICODE_GUILD_ID]
    )

    # Add application commands
    BOT.add_cog(GeneralCommands(BOT))
    BOT.add_cog(ModerationCommands(BOT))
    BOT.add_cog(MiscellaneousCommands(BOT))

    # Run
    BOT.run(BOT_TOKEN)
