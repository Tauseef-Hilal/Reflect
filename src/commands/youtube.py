from html import unescape

from discord import (
    ButtonStyle,
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
    Button,
    select,
    button
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

    # Create command group
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Searching for video(s) {emoji}",
                color=Colors.GOLD
            )
        )

        # Make API call
        search_res = self._bot.youtube.search(query)

        # In case the single arg is True
        if single:

            # Grab video ID
            video_id = ("https://www.youtube.com/watch?v="
                        + search_res[0]["id"]["videoId"])

            # Send single result
            await res.edit_original_message(
                content=f"[||...||]({video_id})",
                embed=None
            )
            return

        # Create a dictionary of videos
        videos: dict[str, Embed] = {}
        youtube_logo = self._bot.emoji_group.get_emoji("youtube")

        # Create embeds for videos
        for video_id in search_res:

            # Setup video details
            title = unescape(video_id["snippet"]["title"])
            channel_title = video_id["snippet"]["channelTitle"]
            description = video_id["snippet"]["description"]
            thumbnail = video_id["snippet"]["thumbnails"]["default"]["url"]
            url = ("https://www.youtube.com/watch?v="
                   f"{video_id['id']['videoId']}")

            # Create embed
            videos[url] = Embed(
                title=title,
                description=f"{description}",
                url=url,
                color=Color(Colors.RED)
            ).set_thumbnail(
                url=thumbnail
            ).set_footer(
                text=channel_title,
                icon_url=youtube_logo.url
            )

        # Send videos with a View obj
        await res.edit_original_message(
            content="Here is what I found:",
            embeds=list(videos.values())[:5],
            view=SelectOptions(self._bot, ctx, videos)
        )


class SelectOptions(View):

    def __init__(self, bot: ICodeBot, ctx: ApplicationContext, videos: dict):
        """
        Initialize

        Args:
            bot (ICodeBot)
            videos (dict): Video dicts
        """
        super().__init__(timeout=360)

        # Set attributes
        self._bot = bot
        self.ctx = ctx
        self.videos = videos
        self.visible_urls = list(videos)[:5]
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

        # Get video URL
        url = self.visible_urls[int(select.values[0])]

        # If its not a followup
        if not self.followup:

            # Send followup msg
            self.followup = await self.ctx.send_followup(
                content=f"[||...||]({url})",
                embeds=[]
            )
            return

        # Otherwise edit the previously sent followup msg
        await self.followup.edit(
            content=f"[||...||]({url})",
            embeds=[]
        )

    @button(
        label="<",
        style=ButtonStyle.primary
    )
    async def left_btn_callback(
        self,
        btn: Button,
        interaction: Interaction
    ) -> None:
        """
        Left button

        Args:
            btn (Button): Button
            interaction (Interaction)
        """

        # Determine the corresponding video idx
        first_idx = list(self.videos).index(self.visible_urls[0])

        if not (first_idx - 4 >= 0):
            return

        # Get visible urls
        self.visible_urls = list(self.videos)[first_idx - 5:first_idx]

        # Send video embeds
        await self.ctx.interaction.edit_original_message(
            embeds=list(self.videos.values())[first_idx - 5:first_idx]
        )

    @button(
        label=">",
        style=ButtonStyle.primary
    )
    async def right_btn_callback(
        self,
        btn: Button,
        interaction: Interaction
    ) -> None:
        """
        Right button

        Args:
            btn (Button): Button
            interaction (Interaction)
        """

        # Get last index
        last_idx = list(self.videos).index(self.visible_urls[-1])

        if not (last_idx + 6 <= len(self.videos)):
            return

        # Get visible urls
        self.visible_urls = list(self.videos)[last_idx + 1:last_idx + 6]

        # Send video embeds
        await self.ctx.interaction.edit_original_message(
            embeds=list(self.videos.values())[last_idx + 1:last_idx + 6]
        )