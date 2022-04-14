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

from ..bot import ICodeBot
from ..utils.color import Colors
from .general import (
    under_maintenance,
    has_permissions
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

    @slash_command(
        name="purge",
        description="Delete a specified number of messages\n"
                    "Usage: `/purge <count> [from_user]`"
    )
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

        # Check if the command invoker has the required permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"manage_messages": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

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

    @slash_command(
        name="kick",
        description="Kick a member from the guild\n"
                    "Usage: `/kick <member> [reason]`"
    )
    async def _kick(
            self,
            ctx: ApplicationContext,
            member: Option(Member, "The member to be kicked"),
            reason: Option(str, "Reason for kick") = ""
    ) -> None:
        """
        Kick a memeber from the guild

        Args:
            ctx (ApplicationContext)
            member (Member): Member to be kicked
        """

        # Check for permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"kick_members": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # Kick the member if its not the owner
        if not member == ctx.guild.owner:
            await member.kick(reason=reason)

            # Send log to staff channel
            emoji = self._bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was kicked out by {ctx.author}\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self._bot.STAFF_CHANNEL.send(embed=embed)

        # Show error message if the member to be kicked is th owner
        else:
            emoji = self._bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission error {emoji}",
                    description=f"You can't kick the owner",
                    color=Colors.RED
                ),
                delete_after=3
            )

            # Send log to staff channel
            emoji = self._bot.emoji_group.get_emoji("warning")
            await self._bot.STAFF_CHANNEL.send(
                embed=Embed(
                    title=f"Alert",
                    description=f"{member} tried to kick the owner!",
                    color=Colors.RED
                ).set_thumbnail(url=emoji.url)
            )

    @slash_command(
        name="ban",
        description="Ban a member from the guild\n"
                    "Usage: `/Ban <member> [reason]`"
    )
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

        # Check for permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"ban_members": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # Ban the member if not owner
        if not member == ctx.guild.owner:
            await member.ban(delete_message_days=0, reason=reason)

            # Send log to the staff channel
            emoji = self._bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was banned by {ctx.author}\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self._bot.STAFF_CHANNEL.send(embed=embed)

        # Otherwise show error message
        else:
            emoji = self._bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission error {emoji}",
                    description=f"You can't ban the owner",
                    color=Colors.RED
                ),
                delete_after=3
            )

            # Send log to staff channel
            emoji = self._bot.emoji_group.get_emoji("warning")
            await self._bot.STAFF_CHANNEL.send(
                embed=Embed(
                    title=f"Alert",
                    description=f"{member} tried to ban the owner!",
                    color=Colors.RED
                ).set_thumbnail(url=emoji.url)
            )

    @slash_command(
        name="timeout",
        description="Timeout a member from the guild\n"
                    "Usage: `/timeout <member> <duration> [reason]`"
    )
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

        # Check for permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"kick_members": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

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

        # Timeout the user if not owner
        if not member == ctx.guild.owner:
            await member.timeout_for(
                duration=timedelta(minutes=duration),
                reason=reason
            )

            # Send log to staff channel
            emoji = self._bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was timed out by {ctx.author} for "
                            f"{duration} minutes\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self._bot.STAFF_CHANNEL.send(embed=embed)

        # Otherwise show error message
        else:
            emoji = self._bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission error {emoji}",
                    description=f"You can't timeout the owner",
                    color=Colors.RED
                ),
                delete_after=3
            )

            # Send log to staff channel
            emoji = self._bot.emoji_group.get_emoji("warning")
            await self._bot.STAFF_CHANNEL.send(
                embed=Embed(
                    title=f"Alert",
                    description=f"{member} tried to timeout the owner!",
                    color=Colors.RED
                ).set_thumbnail(url=emoji.url)
            )

    @slash_command(
        name="lock",
        description="Lock current channel\n"
                    "Usage: `/lock`"
    )
    async def _lock(self, ctx: ApplicationContext) -> None:
        """
        Lock current channel

        Args:
            ctx (ApplicationContext)
        """

        # Check for permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"manage_permissions": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

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

    @slash_command(
        name="unlock",
        description="Unlock current channel\n"
                    "Usage: `/unlock`"
    )
    async def _unlock(self, ctx: ApplicationContext) -> None:
        """
        Unlock current channel

        Args:
            ctx (ApplicationContext)
        """

        # Check for permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"manage_permissions": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

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
