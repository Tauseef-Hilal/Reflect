from html import unescape

from discord import (
    Cog,
    Color,
    Embed,
    Interaction,
    InteractionResponse,
    Option,
    SelectMenu,
    SelectOption,
    SlashCommandGroup,
    ApplicationContext,
)
from discord.ui import (
    View,
    select
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
        query: Option(str, "Search query"),
        single: Option(bool, "Set this to True if you want 1 result") = False
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
                description=f"Searching for video(s) {emoji}",
                color=Colors.GOLD
            )
        )

        videos = self._bot.youtube.search(query)

        if single:
            url = ("https://www.youtube.com/watch?v="
                   + videos[0]["id"]["videoId"])
            await res.edit_original_message(
                content=f"[||...||]({url})",
                embed=None
            )
            return

        embeds = []
        urls = []
        youtube_logo = self._bot.emoji_group.get_emoji("youtube")
        for video in videos:
            url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            title = unescape(video["snippet"]["title"])
            channel_title = video["snippet"]["channelTitle"]
            description = video["snippet"]["description"]
            thumbnail = video["snippet"]["thumbnails"]["default"]["url"]

            urls.append(url)
            embeds.append(
                Embed(
                    title=f"{len(urls)}. {title}",
                    description=f"{description}",
                    url=url,
                    color=Color(Colors.RED)
                ).set_thumbnail(
                    url=thumbnail
                ).set_footer(
                    text=channel_title,
                    icon_url=youtube_logo.url
                )
            )

        await res.edit_original_message(
            content="Here is what I found:",
            embeds=embeds,
            view=SelectOptions(self._bot, ctx, urls)
        )


class SelectOptions(View):

    def __init__(self, bot: ICodeBot, ctx: ApplicationContext, urls: list):
        """
        Initialize

        Args:
            bot (ICodeBot)
            urls (list): List of video urls
        """
        super().__init__(timeout=360)
        self._bot = bot
        self.ctx = ctx
        self.urls = urls
        self.followup = None

    @select(
        placeholder="Select a video",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label="1",
                value="0"
            ),
            SelectOption(
                label="2",
                value="1"
            ),
            SelectOption(
                label="3",
                value="2"
            ),
            SelectOption(
                label="4",
                value="3"
            ),
            SelectOption(
                label="5",
                value="4"
            )
        ]
    )
    async def select_callback(
            self,
            select: SelectMenu,
            interaction: InteractionResponse
    ) -> None:
        """
        Video selection menu

        Args:
            select (SelectMenu)
            interaction (InteractionResponse)
        """

        url = self.urls[int(select.values[0])]

        if not self.followup:
            self.followup = await self.ctx.send_followup(
                content=f"[||...||]({url})",
                embeds=[]
            )
            return

        await self.followup.edit(
            content=f"[||...||]({url})",
            embeds=[]
        )
