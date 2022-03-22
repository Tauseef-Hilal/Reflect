import logging

from discord.ext.commands import Cog
from discord import ApplicationContext, Embed, slash_command

from .constants.color import Colors


class CommandGroup(Cog):
    """
    Group of slash commands
    """

    def __init__(self, bot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self.BOT = bot

    @slash_command()
    async def echo(self, ctx: ApplicationContext, message: str) -> None:
        """
        Echoes a message

        Args:
            ctx (ApplicationContext)
            message (str): Message sent by some user
        """

        logging.info(f"Echo to {ctx.author.name}")
        await ctx.respond(embed=Embed(title=message, color=Colors.BLUE))
