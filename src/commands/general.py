import asyncio
import logging
from datetime import (
    datetime,
)

from discord import (
    Embed,
    Guild,
    Member,
    Message,
    Option,
    Interaction,
    Status,
    AllowedMentions,
    ApplicationContext
)
from discord.ext.commands import (
    Cog,
    slash_command
)

from ..bot import ICodeBot
from ..utils.color import Colors
from ..utils.emoji import EmojiGroup
from ..utils.constants import ANNOUNCEMENTS_CHANNEL_ID
from ..utils.checks import (
    permission_check,
    maintenance_check
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

        def check(message: Message) -> bool:
            return (message.author == ctx.author and
                    message.channel == ctx.channel)

        try:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    title="Embed Title",
                    description="Please provide a title for the embed",
                    color=Colors.BLUE
                )
            )
            msg1: Message = await res.original_message()

            title: Message = await self._bot.wait_for("message",
                                                      check=check,
                                                      timeout=60.0)

            msg2: Message = await ctx.send(
                embed=Embed(
                    title="Embed Description",
                    description="Please provide a description for the embed",
                    color=Colors.BLUE)
            )
            desc: Message = await self._bot.wait_for("message",
                                                     check=check,
                                                     timeout=300.0)

        except asyncio.TimeoutError:
            await ctx.send(embed=Embed(title="TIMEOUT",
                                       description="No response in time",
                                       color=Colors.RED))

        else:
            embed = Embed(title=title.content,
                          description=desc.content,
                          timestamp=datetime.now(),
                          color=Colors.GREEN)

            if ctx.channel_id == ANNOUNCEMENTS_CHANNEL_ID:
                embed = embed.set_footer(text="iCODE Staff",
                                         icon_url=self._bot.user.avatar)

                await ctx.send(content="@everyone",
                               embed=embed,
                               allowed_mentions=AllowedMentions.all())
            else:
                embed = embed.set_footer(text=ctx.author.name,
                                         icon_url=ctx.author.avatar)

                await ctx.send(content=ctx.author.mention,
                               embed=embed)

            await msg1.delete()
            await title.delete()
            await msg2.delete()
            await desc.delete()

    @slash_command(name="update-emojis")
    @maintenance_check()
    async def _update_emojis(self, ctx: ApplicationContext) -> None:
        """
        Update server emojis.

        Args:
            ctx (ApplicationContext)
        """

        logging.info("Updating server emojis")

        # Send `loading` embed
        emojis: EmojiGroup = self._bot.emoji_group
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Updating emojis "
                            f"{emojis.get_emoji('loading_dots')}",
                color=Colors.GOLD
            )
        )
        res_msg: Message = await res.original_message()

        # Update emoji_group
        self._bot.emoji_group.update_emojis()

        # For fun
        await asyncio.sleep(1)

        # Send `done` embed
        await res_msg.edit(
            embed=Embed(
                description=f"Emojis updated {emojis.get_emoji('done')}",
                color=Colors.GREEN
            ),
            delete_after=2
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

        # Suggestions channel
        try:
            collection = self._bot.db.get_collection(str(ctx.guild.id))
            channel = self._bot.get_channel(
                collection.find_one()["channel_ids"]["suggestions_channel"]
            )
        except KeyError:
            logging.warning("Suggestions channel not set")

            emoji = self._bot.emoji_group.get_emoji("warning")
            for channel in self._bot. \
                    get_guild(int(collection.name)).text_channels:
                if channel.can_send(Embed(title="1")):
                    break

            await channel.send(
                embed=Embed(
                    description=f"{emoji} Suggestions channel is not set up. "
                                "Please set it up first using `/setup` "
                                "using `/setup` command.",
                    color=Colors.RED
                )
            )
            return

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

        card = card.add_field(
            name=f"Members - {guild.member_count}",
            value=f":bust_in_silhouette: {humans} - :robot: {bots}"
        )

        normal, animated = 0, 0
        for emoji in guild.emojis:
            if emoji.animated:
                animated += 1
                continue

            normal += 1

        ukraine = self._bot.emoji_group.get_emoji("ukraine")
        blob = self._bot.emoji_group.get_emoji("blob_on_drugs")
        card = card.add_field(
            name=f"Emojis - {len(guild.emojis)}",
            value=f"{ukraine} {normal} - {blob} {animated}"
        )

        human, bot = 0, 0
        for role in guild.roles:
            if role.is_bot_managed():
                bot += 1
                continue

            human += 1

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

        # Confirm params
        if not user:
            user: Member = ctx.guild.get_member(ctx.author.id)

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

        # First line
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

        status: Status = user.status
        if user.is_on_mobile() and status.name == "online":
            status_emoji = self._bot.emoji_group.get_emoji("mobile")
        else:
            status_emoji = self._bot.emoji_group.get_emoji(status.name)

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
