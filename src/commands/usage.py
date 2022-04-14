import asyncio
import logging
from datetime import (
    datetime,
)

from discord import (
    Embed,
    Guild,
    InteractionResponse,
    Member,
    Message,
    Option,
    Permissions,
    Interaction,
    SelectMenu,
    SelectOption,
    Status,
    TextChannel,
    AllowedMentions,
    ApplicationContext
)
from discord.ui import (
    View,
    select
)
from discord.ext.commands import (
    Cog,
    slash_command
)

from ..bot import ICodeBot
from ..utils.color import Colors

class Help(Cog):
    """
    Help command
    """

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @slash_command(name="help")
    async def _help(self, ctx: ApplicationContext) -> None:
        """
        Show usage help

        Args:
            ctx (ApplicationContext)
        """

        embed = Embed(
            description=self._bot.description,
            color=Colors.GOLD,
            timestamp=datetime.now()
        ).set_author(
            name="iCODE Usage Help",
            icon_url=self._bot.user.display_avatar
        ).set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ).set_thumbnail(
            url=self._bot.user.display_avatar
        )

        await ctx.respond(
            embed=embed,
            view=UsageView(self._bot, ctx)
        )


class UsageView(View):

    def __init__(self, bot: ICodeBot, ctx: ApplicationContext):
        """
        Initialize

        Args:
            bot (ICodeBot)
            ctx (ApplicationContext)
        """
        super().__init__(timeout=360)
        self._bot = bot
        self.ctx = ctx

    @select(
        placeholder="Select command type",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label="General Commands",
                value="GeneralCommands"
            ),
            SelectOption(
                label="Moderation Commands",
                value="ModerationCommands"
            ),
            SelectOption(
                label="Miscellaneous Commands",
                value="MiscellaneousCommands"
            )
        ]
    )
    async def select_callback(
            self,
            select: SelectMenu,
            interaction: InteractionResponse
    ) -> None:
        """
        Cog selection menu

        Args:
            select (SelectMenu)
            interaction (InteractionResponse)
        """

        cog = self._bot.get_cog(select.values[0])
        desc = cog.description

        embed = Embed(
            description=desc,
            color=Colors.GOLD,
        ).set_author(
            name="iCODE Usage Help",
            icon_url=self._bot.user.display_avatar
        ).set_footer(
            text="<Required> - [Optional]",
            icon_url=self.ctx.author.display_avatar
        ).set_thumbnail(
            url=self._bot.user.display_avatar
        )

        emoji = self._bot.emoji_group.get_emoji("reply")
        for cmd in cog.get_commands():
            embed.add_field(
                name=f"__/{cmd.qualified_name}__",
                value=str(emoji) + cmd.description.replace("\n", f"\n{emoji}"),
                inline=False
            )

        await interaction.response.edit_message(
            embed=embed
        )
