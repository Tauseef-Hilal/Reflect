import logging

from discord import Intents

from .bot import ICodeBot
from .commands.usage import Help
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

    # Setup intents
    intents = Intents.default()
    intents.members = True
    intents.message_content = True
    intents.presences = True

    # Instantiate ICodeBot
    BOT = ICodeBot(
        description="Hi! I'm a bot under development.",
        intents=intents
    )

    # Add application commands
    BOT.add_cog(Help(BOT))
    BOT.add_cog(GeneralCommands(BOT))
    BOT.add_cog(ModerationCommands(BOT))
    BOT.add_cog(MiscellaneousCommands(BOT))

    # Run
    BOT.run(BOT_TOKEN)
