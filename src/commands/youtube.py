from discord import (
    Cog,
    Embed,
    Interaction,
    Option,
    SlashCommandGroup,
    ApplicationContext,
)

from ..utils.color import Colors
from ..bot import ICodeBot
from ..utils.checks import (
    maintenance_check,
)


class YoutubeCommands(Cog):
    """
    Commands for interacting with YouTube API
    """

    YT = SlashCommandGroup(
        "youtube",
        "YouTube commands"
    )

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @YT.command(name="search")
    @maintenance_check()
    async def _search(
        self,
        ctx: ApplicationContext,
        query: Option(str, "Search query")
    ) -> None:
        """
        Search for a YouTube video.

        Args:
            ctx (ApplicationContext)
            query (Option): Search query
            channel (Option): Name of channel/
        """

        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Fetching video data {emoji}",
                color=Colors.GOLD
            )
        )

        urls = self._bot.youtube.search(query)

        await ctx.send(
            content="Here is what I found:\n" + "\n".join(urls)
        )
        await res.delete_original_message()
