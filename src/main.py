import logging

from .bot import ICodeBot
from .commands import CommandGroup
from .constants.env import ICODE_GUILD_ID, BOT_TOKEN


def main() -> None:
    """
        Main
    """

    # Set Up Logging
    FORMAT = "[%(name)s] => [%(levelname)s] : %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    # Initialize
    BOT = ICodeBot(
        description="The BOT made for iCODE Discord server.",
        debug_guilds=[ICODE_GUILD_ID]
    )
    COMMAND_GROUP = CommandGroup(BOT)

    BOT.add_cog(COMMAND_GROUP)
    BOT.run(BOT_TOKEN)
