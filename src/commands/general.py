import asyncio
import logging
from datetime import (
    datetime,
)
from pprint import pprint
from typing import List

from discord import (
    ButtonStyle,
    Embed,
    Guild,
    Member,
    Message,
    Option,
    Interaction,
    Status,
    ApplicationContext,
    TextChannel,
    InputTextStyle
)
from discord.ext.commands import (
    Cog,
    slash_command
)
from discord.ui import (
    Modal,
    InputText,
    View,
    Button,
    select,
    button
)

from ..bot import ICodeBot
from ..utils.color import Colors
from ..utils.emoji import EmojiGroup
from ..utils.constants import ANNOUNCEMENTS_CHANNEL_ID
from ..utils.checks import (
    maintenance_check
)


class EmbedBuilder(Modal):
    """Embed Builder"""

    def __init__(self, ctx: ApplicationContext, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx

        # Add input field for embed title
        self.add_item(InputText(
            style=InputTextStyle.singleline,
            label="Embed Title",
            placeholder="Title",
            required=True
        ))

        # Add input field for embed description
        self.add_item(InputText(
            style=InputTextStyle.paragraph,
            label="Embed Description",
            placeholder="Description",
            required=True
        ))

        # Add input field for embed thumbnail url
        self.add_item(InputText(
            style=InputTextStyle.singleline,
            label="Embed Thumbnail",
            placeholder="Thumbnail URL",
            required=False
        ))

        # Add input field for embed footer
        self.add_item(InputText(
            style=InputTextStyle.singleline,
            label="Embed Footer",
            placeholder="Footer Text",
            required=False
        ))

    async def callback(self, interaction: Interaction):

        # Create Embed object
        embed = Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=Colors.GOLD,
            timestamp=datetime.now()
        )

        # Set thumbnail if provided
        if url := self.children[2].value:
            embed = embed.set_thumbnail(url=url)

        # Set footer if provided
        if footer_text := self.children[3].value:
            embed = embed.set_footer(
                text=footer_text,
                icon_url=self.ctx.author.display_avatar
            )

        # Send embedded message
        await interaction.response.send_message(embed=embed)


class EmojiDisplay(View):

    def __init__(self, bot: ICodeBot, ctx: ApplicationContext, embeds: List):
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
        self.embeds = embeds
        self.cursor = 0

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

        # Return if the cursor is at first embed
        if (self.cursor - 1) < 0:
            await interaction.response.defer();
            return

        # Update cursor
        self.cursor -= 1

        # Send video embeds
        await interaction.response.edit_message(
            embed=self.embeds[self.cursor]
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

        # Return if the cursor is at last embed
        if (self.cursor + 1) >= len(self.embeds) - 1:
            await interaction.response.defer();
            return

        # Update cursor
        self.cursor += 1

        # Send video embeds
        await interaction.response.edit_message(
            embed=self.embeds[self.cursor]
        )


class GeneralCommands(Cog):
    """
    General commands
    """

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @slash_command(name="embed")
    @maintenance_check()
    async def _embed(self, ctx: ApplicationContext) -> None:
        """
        Build an embedded message

        (to be modified in future)

        Args:
            ctx (ApplicationContext)
        """

        # Create instance of EmbedBuilder
        embed_builder: EmbedBuilder = EmbedBuilder(
            ctx,
            title="Embed Builder"
        )

        # Send Embed Builder
        await ctx.send_modal(embed_builder)

    @slash_command(name="emojis")
    @maintenance_check()
    async def _show_emojis(self, ctx: ApplicationContext) -> None:
        """
        Show all available emojis

        Args:
            ctx (ApplicationContext)
        """
        
        # Create a list of available emojis
        emojis: List[str] = [
            f"{self._bot.emoji_group.get_emoji(emoji, id)} • `:{emoji}:`"
            for id, guild_emojis in self._bot.emoji_group._emojis.items()
            for emoji in guild_emojis
        ]

        # To prevent IndexeError
        emoji_count = len(emojis)
        while emoji_count % 20 != 0:
            emojis.append(".")
            emoji_count += 1

        # Create embeds for emojis
        embeds: List[Embed] = []
        for i in range(0, len(emojis), 20):
            embed = Embed(
                color=Colors.GOLD,
                timestamp=datetime.now()
            ).set_author(
                name=f"Reflect - Emojis",
                icon_url=ctx.guild.icon
            ).set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
            ).set_thumbnail(
                url=self._bot.user.display_avatar
            ).add_field(
                name="Column 1",
                value="\n".join(emojis[i:i+10]),
                inline=True
            ).add_field(
                name="Column 2",
                value="\n".join(emojis[i+10:i+20])
            )

            embeds.append(embed)


        # Send embed with a view obj
        await ctx.respond(
            embed=embeds[0],
            view=EmojiDisplay(self._bot, ctx, embeds)
        )

    @slash_command(name="suggest")
    @maintenance_check()
    async def _suggest(
        self,
        ctx: ApplicationContext,
        suggestion: Option(str, "Your suggestion")
    ) -> None:
        """
        Make a suggestion

        Args:
            ctx (ApplicationContext)
        """

        # Try to get Suggestions channel
        try:
            channel = self._bot.get_channel(
                self._bot.db.find_one(
                    {"guild_id": ctx.guild.id}
                )["channel_ids"]["suggestions_channel"]
            )
            assert isinstance(channel, TextChannel)

        # Send message to set up suggestions channel if not successful
        except (KeyError, TypeError, AssertionError):
            logging.warning("Suggestions channel not set")

            emoji = self._bot.emoji_group.get_emoji("warning")
            await ctx.respond(
                embed=Embed(
                    description=f"{emoji} Suggestions channel is not set up. "
                                "Please set it up first using `/setup` "
                                "command.",
                    color=Colors.RED
                )
            )
            return

        # Respond
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Sending suggestion {emoji}",
                color=Colors.GOLD
            ),
        )

        # Reactions to add
        upvote = self._bot.emoji_group.get_emoji("upvote")
        downvote = self._bot.emoji_group.get_emoji("downvote")

        # Send suggestion
        msg: Message = await channel.send(
            embed=Embed(
                description=f"**{suggestion}**\n___",
                color=Colors.GOLD,
                timestamp=datetime.now()
            ).set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
            )
        )

        # Add reactions
        await msg.add_reaction(upvote)
        await msg.add_reaction(downvote)

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Suggestion sent {emoji}",
                color=Colors.GREEN
            ),
            delete_after=3
        )

    @slash_command(name="serverinfo")
    @maintenance_check()
    async def _serverinfo(self, ctx: ApplicationContext) -> None:
        """
        Get information about the server

        Args:
            ctx (ApplicationContext)
        """

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Fetching server data {emoji}",
                color=Colors.GOLD
            )
        )

        # Get guild
        guild: Guild = self._bot.get_guild(ctx.guild.id)

        # Create server card
        card = Embed(
            description=guild.description,
            color=Colors.GOLD,
            timestamp=datetime.now()
        ).set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ).set_author(
            name=f"Server Info",
            icon_url=guild.icon
        ).set_thumbnail(url=guild.icon)

        # First line
        card = card.add_field(
            name="Server Name",
            value=f"{guild}",
            inline=True
        )
        card = card.add_field(
            name="Server ID",
            value=guild.id
        )
        card = card.add_field(
            name="Server Owner",
            value=guild.owner.mention
        )

        # Second line
        humans, bots = 0, 0
        for member in guild.members:
            if member.bot:
                bots += 1
                continue

            humans += 1

        # Add field for members
        card = card.add_field(
            name=f"Members - {guild.member_count}",
            value=f":bust_in_silhouette: {humans} - :robot: {bots}"
        )

        # Calculate the number of animated emojis
        normal, animated = 0, 0
        for emoji in guild.emojis:
            if emoji.animated:
                animated += 1
                continue

            normal += 1

        # Add field for emojis
        ukraine = self._bot.emoji_group.get_emoji("ukraine")
        blob = self._bot.emoji_group.get_emoji("blob_on_drugs")
        card = card.add_field(
            name=f"Emojis - {len(guild.emojis)}",
            value=f"{ukraine} {normal} - {blob} {animated}"
        )

        # Calculate the number of humans and bots
        human, bot = 0, 0
        for role in guild.roles:
            if role.is_bot_managed():
                bot += 1
                continue

            human += 1

        # Add field for roles
        card = card.add_field(
            name=f"Roles - {len(guild.roles)}",
            value=f":bust_in_silhouette: {human} - :robot: {bot}"
        )

        # Third line
        features = ""
        for feature in reversed(sorted(guild.features, key=lambda s: len(s))):
            features += " • "
            features += feature.replace("_", " ").title()
            features += "\n"

        # Add a field for features
        if features:
            card = card.add_field(
                name="Server Features",
                value=features,
                inline=False
            )

        # Send embed
        await res.edit_original_message(embed=card)

    @slash_command(name="icon")
    @maintenance_check()
    async def _icon(self, ctx: ApplicationContext) -> None:
        """
        Get the icon of the server.

        Args:
            ctx (ApplicationContext)
        """

        # Send embed
        await ctx.respond(
            embed=Embed(
                color=ctx.author.color,
                timestamp=datetime.now()
            ).set_image(
                url=ctx.guild.icon
            ).set_author(
                name=f"{ctx.guild}",
                icon_url=ctx.guild.icon
            ).set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
            )
        )

    @slash_command(name="userinfo")
    @maintenance_check()
    async def _userinfo(
        self,
        ctx: ApplicationContext,
        user: Option(
            Member,
            "The user whose info you want. By default, "
            "its the command invoker."
        ) = None
    ) -> None:
        """
        Get information about a user

        Args:
            ctx (ApplicationContext)
            user (Member): The user whose info is to be fetched
        """

        # Validate params
        if not user:
            user: Member = ctx.guild.get_member(ctx.author.id)

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Fetching user data {emoji}",
                color=Colors.GOLD
            )
        )

        # Create user card
        card = Embed(
            color=user.color,
            timestamp=datetime.now()
        ).set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ).set_author(
            name=f"{user} - User Info",
            icon_url=user.display_avatar
        ).set_thumbnail(url=user.display_avatar)

        # Add fields for Tag, ID and Nickname
        card = card.add_field(
            name="User Tag",
            value=f"{user}",
            inline=True
        )
        card = card.add_field(
            name="User ID",
            value=user.id
        )
        card = card.add_field(
            name="Nickname",
            value=user.display_name
        )

        # Second line
        emoji = self._bot.emoji_group.get_emoji(
            "red_cross" if user.bot else "green_tick"
        )

        # Get user's status
        status: Status = user.status
        if user.is_on_mobile() and status.name == "online":
            status_emoji = self._bot.emoji_group.get_emoji("mobile")
        else:
            status_emoji = self._bot.emoji_group.get_emoji(status.name)

        # Add fields more fields
        card = card.add_field(
            name="Active Status",
            value=f"{status_emoji} {status.value.upper()}",
        )
        card = card.add_field(
            name="Human Verified",
            value=f"{emoji} {not user.bot}",
        )
        card = card.add_field(
            name="Top Role",
            value=f"{user.top_role.mention}",
        )

        # Third line
        card = card.add_field(
            name="Current Activity",
            value=user.activity.name if user.activity else "None",
        )
        card = card.add_field(
            name="Account Created On",
            value=user.created_at.strftime("%d %B, %Y"),
        )
        card = card.add_field(
            name="Joined The Server On",
            value=user.joined_at.strftime("%d %B, %Y"),
        )

        await res.edit_original_message(embed=card)

    @slash_command(name="avatar")
    @maintenance_check()
    async def _avatar(
        self,
        ctx: ApplicationContext,
        user: Option(
            Member,
            "The user whose avatar you want to get. By default, "
            "its the command invoker"
        ) = None
    ) -> None:
        """
        Get a user's avatar

        Args:
            ctx (ApplicationContext):
            user (Option, optional): The user whose avatar you want. Defaults to None.
        """

        # Confirm params
        if not user:
            user: Member = ctx.guild.get_member(ctx.author.id)

        # Send embed
        await ctx.respond(
            embed=Embed(
                color=user.color,
                timestamp=datetime.now()
            ).set_image(
                url=user.display_avatar
            ).set_author(
                name=f"{user}",
                icon_url=user.display_avatar
            ).set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
            )
        )

    @slash_command(name="membercount")
    @maintenance_check()
    async def _membercount(self, ctx: ApplicationContext) -> None:
        """
        Get the number of members in the guild.

        Args:
            ctx (ApplicationContext)
        """

        member: Member
        guild: Guild = ctx.guild
        total, humans, bots = 0, 0, 0

        # Calculate
        for member in guild.members:
            if member.bot:
                bots += 1
            else:
                humans += 1

            total += 1

        # Create embed
        await ctx.respond(
            embed=Embed(
                color=ctx.author.color,
                timestamp=datetime.now()
            ).set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
            ).set_thumbnail(
                url=guild.icon
            ).add_field(
                name="Humans",
                value=f"{humans}"
            ).add_field(
                name="Bots",
                value=f"{bots}"
            ).add_field(
                name="Total Members",
                value=f"{total}",
                inline=False
            )
        )
