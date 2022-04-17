import asyncio
from datetime import (
    datetime,
    timedelta
)

from discord import (
    Cog,
    Embed,
    Option,
    Member,
    Message,
    Interaction,
    TextChannel,
    ApplicationContext
)
from discord.ext.commands import (
    slash_command
)
from discord.errors import Forbidden

from ..bot import ICodeBot
from ..utils.color import Colors
from ..utils.checks import (
    maintenance_check,
    permission_check
)


class ModerationCommands(Cog):
    """
    Moderation commands
    """

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @slash_command(name="purge")
    @maintenance_check()
    @permission_check(kick_members=True)
    async def _purge(
        self,
        ctx: ApplicationContext,
        count: Option(str, "Number of messages to delete"),
        from_user: Option(Member, "Delete a single user's messages") = None
    ) -> None:
        """
        Delete a specified number of messages

        Args:
            ctx (ApplicationContext):
            count (MessageCountConverter): Number of messages to delete
        """

        # Determine the integer value of count
        if count == "all":
            count = -1
        else:
            try:
                count = int(count)

            # Send error message to the user if unsuccessful
            except ValueError:
                emoji = self._bot.emoji_group.get_emoji("red_cross")
                await ctx.respond(
                    embed=Embed(
                        title=f"Invalid arguments {emoji}",
                        description="`count` must be an integer in [-1, ∞)"
                                    " or string `all`",
                        color=Colors.RED
                    ),
                    delete_after=3
                )
                return

        # Record current time so that we delete only the messages
        # which were sent befor this time
        invoking_time = datetime.now()

        # Just for fun
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Fetching messages {emoji}",
                color=Colors.GOLD
            )
        )
        await asyncio.sleep(1)

        await res.edit_original_message(
            embed=Embed(
                description=f"Deleting message(s) {emoji}",
                color=Colors.GOLD
            )
        )

        # Delete the messages
        channel: TextChannel = ctx.channel
        deleted: list[Message] = await channel.purge(
            limit=None if count == -1 else count,
            check=lambda msg: (msg.author == from_user) if from_user else True,
            before=invoking_time
        )

        # Show success msg to user
        emoji = self._bot.emoji_group.get_emoji("done")
        await res.edit_original_message(
            embed=Embed(
                description=f"{len(deleted)} message(s) deleted {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @slash_command(name="kick")
    @maintenance_check()
    @permission_check(kick_members=True)
    async def _kick(
            self,
            ctx: ApplicationContext,
            member: Option(Member, "The member to be kicked"),
            reason: Option(str, "Reason for kick") = ""
    ) -> None:
        """
        Kick a member from the guild

        Args:
            ctx (ApplicationContext)
            member (Member): Member to be kicked
        """

        # Kick the member
        try:
            await member.kick(reason=reason)
        except Forbidden:
            emoji = ctx.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission Error {emoji}",
                    description="I do not have the required permissions"
                                " to run this command.",
                    color=Colors.RED
                ),
                delete_after=3
            )
            return

        # Send log to staff channel
        emoji = self._bot.emoji_group.get_emoji("rules")
        embed = Embed(
            description=f"{member.mention} was kicked out by "
                        f"{ctx.author.mention}",
            color=Colors.RED,
            timestamp=datetime.now()
        ).add_field(
            name="Reason",
            value=f"{reason if reason else 'No reason provided.'}"
        ).set_author(
            name="Modlogs",
            icon_url=self._bot.user.display_avatar
        ).set_thumbnail(url=emoji.url)

        await ctx.respond(embed=embed, delete_after=3)

        try:
            collection = self._bot.db.get_collection(str(ctx.guild_id))
            channel = self._bot.get_channel(
                collection.find_one()["channel_ids"]["modlogs_channel"]
            )
        except KeyError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await ctx.channel.send(
                embed=Embed(
                    description=f"{emoji} No channel is set for modlogs. "
                                "Please setup a channel for modlogs "
                                "by using `/setup` command",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        await channel.send(embed=embed)

    @slash_command(name="ban")
    @maintenance_check()
    @permission_check(ban_members=True)
    async def _ban(
            self,
            ctx: ApplicationContext,
            member: Option(Member, "The member to be banned"),
            reason: Option(str, "Reason for ban") = ""
    ) -> None:
        """
        Ban a memeber from the guild

        Args:
            ctx (ApplicationContext)
            member (Member): Member to be banned
        """

        # Ban the member
        try:
            await member.ban(reason=reason)
        except Forbidden:
            emoji = ctx.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission Error {emoji}",
                    description="I do not have the required permissions"
                                " to run this command.",
                    color=Colors.RED
                ),
                delete_after=3
            )
            return

        # Send log to staff channel
        emoji = self._bot.emoji_group.get_emoji("rules")
        embed = Embed(
            description=f"{member.mention} was banned by "
                        f"{ctx.author.mention}",
            color=Colors.RED,
            timestamp=datetime.now()
        ).add_field(
            name="Reason",
            value=f"{reason if reason else 'No reason provided.'}"
        ).set_author(
            name="Modlogs",
            icon_url=self._bot.user.display_avatar
        ).set_thumbnail(url=emoji.url)

        await ctx.respond(embed=embed, delete_after=3)

        try:
            collection = self._bot.db.get_collection(str(ctx.guild_id))
            channel = self._bot.get_channel(
                collection.find_one()["channel_ids"]["modlogs_channel"]
            )
        except KeyError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await ctx.channel.send(
                embed=Embed(
                    description=f"{emoji} No channel is set for modlogs. "
                                "Please setup a channel for modlogs "
                                "by using `/setup` command",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        await channel.send(embed=embed)

    @slash_command(name="timeout")
    @maintenance_check()
    @permission_check(kick_members=True)
    async def _timeout(
            self,
            ctx: ApplicationContext,
            member: Option(Member, "The member to be timed out"),
            duration: Option(int, "Duration in minutes"),
            reason: Option(str, "Reason for timeout") = ""
    ) -> None:
        """
        Timeout a member from the guild

        Args:
            ctx (ApplicationContext)
            member (Member): Member to be kicked
        """

        # Show error message if the user is already timed out
        if member.timed_out:
            emoji = self._bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Command error {emoji}",
                    description="The member is already timed out"
                )
            )
            return

        # Timeout the user
        try:
            await member.timeout_for(
                duration=timedelta(minutes=duration),
                reason=reason
            )
        except Forbidden:
            emoji = ctx.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission Error {emoji}",
                    description="I do not have the required permissions"
                                " to run this command.",
                    color=Colors.RED
                ),
                delete_after=3
            )
            return

        # Send log to staff channel
        emoji = self._bot.emoji_group.get_emoji("rules")
        embed = Embed(
            description=f"{member.mention} was timed out by "
                        f"{ctx.author.mention}",
            color=Colors.RED,
            timestamp=datetime.now()
        ).add_field(
            name="Reason",
            value=f"{reason if reason else 'No reason provided.'}"
        ).set_author(
            name="Modlogs",
            icon_url=self._bot.user.display_avatar
        ).set_thumbnail(url=emoji.url)

        await ctx.respond(embed=embed, delete_after=3)

        try:
            collection = self._bot.db.get_collection(str(ctx.guild_id))
            channel = self._bot.get_channel(
                collection.find_one()["channel_ids"]["modlogs_channel"]
            )
        except KeyError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await ctx.channel.send(
                embed=Embed(
                    description=f"{emoji} No channel is set for modlogs. "
                                "Please setup a channel for modlogs "
                                "by using `/setup` command",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        await channel.send(embed=embed)

    @slash_command(name="lock")
    @maintenance_check()
    @permission_check(manage_permissions=True)
    async def _lock(self, ctx: ApplicationContext) -> None:
        """
        Lock current channel

        Args:
            ctx (ApplicationContext)
        """

        # Get the channel from which the command was invoked
        channel: TextChannel = ctx.channel

        # Show error message if already locked
        if not channel.permissions_for(ctx.guild.default_role).send_messages:
            emoji = self._bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    description=f"Channel is already locked {emoji}",
                    color=Colors.RED
                ),
                delete_after=2
            )
            return

        # Otherwise lock the channel
        await channel.set_permissions(
            target=ctx.guild.default_role,
            send_messages=False
        )

        # Show success message
        emoji = self._bot.emoji_group.get_emoji("done")
        await ctx.respond(
            embed=Embed(
                description=f"Channel locked {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @slash_command(name="unlock")
    @maintenance_check()
    @permission_check(manage_permissions=True)
    async def _unlock(self, ctx: ApplicationContext) -> None:
        """
        Unlock current channel

        Args:
            ctx (ApplicationContext)
        """

        # Get the channel from which the command was invoked
        channel: TextChannel = ctx.channel

        # Show error message if already unlocked
        if channel.permissions_for(ctx.guild.default_role).send_messages:
            emoji = self._bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    description=f"Channel is already unlocked {emoji}",
                    color=Colors.RED
                ),
                delete_after=2
            )
            return

        # Otherwise unlock the channel
        await channel.set_permissions(
            target=ctx.guild.default_role,
            send_messages=True
        )

        # Send success message
        emoji = self._bot.emoji_group.get_emoji("done")
        await ctx.respond(
            embed=Embed(
                description=f"Channel unlocked {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
