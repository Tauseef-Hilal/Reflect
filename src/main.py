import logging

from discord import Intents


from .bot import Reflect
from .commands.usage import Help
from .commands.setup import SetupCommands
from .commands.youtube import YoutubeCommands
from .commands.general import GeneralCommands
from .commands.moderation import ModerationCommands
from .commands.miscellaneous import MiscellaneousCommands
from .commands.reaction_roles import ReactionRoleCommands
from .utils.env import (
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
    intents.guilds = True

    # Instantiate ICodeBot
    BOT = Reflect(
        description="Hi! I'm a bot under development.",
        intents=intents
    )

    # Add application commands
    BOT.add_cog(Help(BOT))
    BOT.add_cog(SetupCommands(BOT))
    BOT.add_cog(YoutubeCommands(BOT))
    BOT.add_cog(GeneralCommands(BOT))
    BOT.add_cog(ModerationCommands(BOT))
    BOT.add_cog(MiscellaneousCommands(BOT))
    BOT.add_cog(ReactionRoleCommands(BOT))

    # Run
    BOT.run(BOT_TOKEN)
