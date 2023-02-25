import asyncio
import logging

from discord import (
    Game,
    Embed,
    Status,
    Message,
    Interaction,
    ApplicationContext
)
from discord.ext.commands import (
    Cog,
    slash_command
)



from ..bot import Reflect
from ..utils.color import Colors
from ..utils.checks import (
    maintenance_check,
    permission_check
)


class MiscellaneousCommands(Cog):
    """
    Miscellaneous commands    
    """

    def __init__(self, bot: Reflect) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @slash_command(name="toggle-maintenance-mode")
    @permission_check(bot_owner=True)
    async def _toggle_maintenance_mode(self, ctx: ApplicationContext) -> None:
        """
        Turn maintenance mode on or off

        Args:
            ctx (ApplicationContext)
        """

        # Respond with an embed and toggle maintenance mode
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        if self._bot.MAINTENANCE_MODE:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    description=f"Disabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self._bot.change_presence(
                status=Status.online,
                activity=Game(name="/emojis | .py")
            )

        else:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    description=f"Enabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self._bot.change_presence(
                status=Status.do_not_disturb,
                activity=Game(name="| Under Maintenance")
            )

        # Toggle maintenance mode
        self._bot.MAINTENANCE_MODE = not self._bot.MAINTENANCE_MODE
        await asyncio.sleep(1)

        # Prompt completion
        emoji = self._bot.emoji_group.get_emoji("done")
        msg: Message = await res.original_response()

        await msg.edit(
            embed=Embed(
                description=f"Toggled maintenance mode {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
        logging.info("Toggled maintenance mode")
