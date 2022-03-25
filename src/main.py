import logging
import sys

from discord import Intents

from .bot import ICodeBot
from .commands import CommandGroup
from .utils.env import ICODE_GUILD_ID, BOT_TOKEN


def usage() -> None:
    """
    Print usage
    """

    print("USAGE: python3 run.py [ maintenance:[on | off] ]")
    sys.exit()


def main() -> None:
    """
        Main
    """
    MAINTENANCE = False

    # Determine MAINTENANCE value
    if len(sys.argv) > 2:
        usage()
    elif sys.argv[-1] == "maintenance:on":
        MAINTENANCE = True

    # Set Up Logging
    FORMAT = "[%(name)s] => [%(levelname)s] : %(message)s"
    if MAINTENANCE:
        FORMAT = "(MAINTENANCE-MODE) " + FORMAT

    logging.basicConfig(level=logging.INFO, format=FORMAT)

    # Initialize
    INTENTS = Intents.all()

    BOT = ICodeBot(
        description="The BOT made for iCODE Discord server.",
        maintenance=MAINTENANCE,
        intents=INTENTS,
        debug_guilds=[ICODE_GUILD_ID]
    )
    COMMAND_GROUP = CommandGroup(BOT)

    BOT.add_cog(COMMAND_GROUP)
    BOT.run(BOT_TOKEN)
