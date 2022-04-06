import sys
import asyncio
import logging
from io import StringIO
from datetime import (
    datetime,
    timedelta
)

from discord import (
    Game,
    Embed,
    Option,
    Status,
    Member,
    Message,
    Permissions,
    Interaction,
    TextChannel,
    AllowedMentions,
    ApplicationContext
)
from discord.ext.commands import (
    Cog,
    slash_command
)


from .bot import ICodeBot
from .utils.color import Colors
from .utils.emoji import EmojiGroup
from .utils.constants import ANNOUNCEMENTS_CHANNEL_ID


class CommandGroup(Cog):
    """
    Group of slash commands
    """

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self.bot = bot

    def _under_maintenance(self, channel: TextChannel) -> bool:
        """
        Check if the bot is under maintenance

        Args:
            `channel` (TextChannel): The channel from which a cmd was run

        Returns:
            bool: True if under maintenance
        """

        return (self.bot.MAINTENANCE_MODE and
                channel != self.bot.MAINTENANCE_CHANNEL)

    async def _has_permissions(self, ctx: ApplicationContext, **perms) -> bool:
        """
        Check whether a member has required permissions to
        run a command

        Returns:
            bool: True if the member has all of the perms
        """

        # Get channel and permissions of the author in that channel
        channel: TextChannel = ctx.channel
        permissions: Permissions = channel.permissions_for(ctx.author)

        # Find missing permissions
        missing = [perm for perm, value in perms.items()
                   if getattr(permissions, perm) != value]

        # Return true if the author has all the required permissions
        if not missing:
            return True

        # Otherwise show error message to the member
        emoji = self.bot.emoji_group.get_emoji("red_cross")
        await ctx.respond(
            embed=Embed(
                title=f"Permission Error {emoji}",
                description="You do not have the permission"
                            " to run this command",
                color=Colors.RED
            ),
            delete_after=3
        )

        return False

    @slash_command(name="embed")
    async def _embed(self, ctx: ApplicationContext) -> None:
        """
        Command for building embeds

        (to be modified in future)

        Args:
            ctx (ApplicationContext)
        """

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if self._under_maintenance(ctx.channel):
            self.bot.dispatch("maintenance", ctx)
            return

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

            title: Message = await self.bot.wait_for("message",
                                                     check=check,
                                                     timeout=60.0)

            msg2: Message = await ctx.send(
                embed=Embed(
                    title="Embed Description",
                    description="Please provide a description for the embed",
                    color=Colors.BLUE)
            )
            desc: Message = await self.bot.wait_for("message",
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
                                         icon_url=self.bot.user.avatar)

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
    async def _update_emojis(self, ctx: ApplicationContext) -> None:
        """
        Update server emojis. Run this command after adding new emojis

        Args:
            ctx (ApplicationContext)
        """

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if self._under_maintenance(ctx.channel):
            self.bot.dispatch("maintenance", ctx)
            return

        logging.info("Updating server emojis")

        # Send `loading` embed
        emojis: EmojiGroup = self.bot.emoji_group
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Updating emojis "
                            f"{emojis.get_emoji('loading_dots')}",
                color=Colors.GOLD
            )
        )
        res_msg: Message = await res.original_message()

        # Update emoji_group
        self.bot.emoji_group.update_emojis()

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

    @slash_command(name="emojis")
    async def _list_emojis(self, ctx: ApplicationContext) -> None:
        """
        List available emojis

        Args:
            ctx (ApplicationContext)
        """

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if self._under_maintenance(ctx.channel):
            self.bot.dispatch("maintenance", ctx)
            return

        # Create embed
        embed = Embed(
            title="Server Emojis",
            description="Everyone can use below listed emojis!",
            timestamp=datetime.now(),
            color=Colors.GOLD
        )

        # Add normal emojis to the embed
        emoji_group = self.bot.emojis
        emojis = [f"{emoji} • `:{emoji.name}:`"
                  for emoji in emoji_group if not emoji.animated]

        embed = embed.add_field(name="Normal Emojis", value="\n".join(emojis))

        # Add animated emojis to the embed
        emojis = [f"{emoji} • `:{emoji.name}:`"
                  for emoji in emoji_group if emoji.animated]

        embed = embed.add_field(name="Animated Emojis",
                                value="\n".join(emojis))

        # Set embed footer
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        # Set embed thumbnail
        embed.set_thumbnail(url=self.bot.emoji_group.get_emoji("ukraine").url)

        # Send embed
        await ctx.respond(embed=embed)

    @slash_command(name="toggle-maintenance-mode")
    async def _toggle_maintenance_mode(self, ctx: ApplicationContext) -> None:
        """
        Turn maintenance mode on or off

        Args:
            ctx (ApplicationContext)
        """

        # Check
        if not await self._has_permissions(ctx, **{"administrator": True}):
            return

        # Respond with an embed and toggle maintenance mode
        emoji = self.bot.emoji_group.get_emoji("loading_dots")
        if self.bot.MAINTENANCE_MODE:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    description=f"Disabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self.bot.change_presence(activity=Game(name="/emojis | .py"))

        else:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    description=f"Enabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self.bot.change_presence(
                status=Status.do_not_disturb,
                activity=Game(name="| Under Maintenance")
            )

        # Toggle maintenance mode
        self.bot.MAINTENANCE_MODE = not self.bot.MAINTENANCE_MODE
        await asyncio.sleep(1)

        # Prompt completion
        emoji = self.bot.emoji_group.get_emoji("done")
        msg: Message = await res.original_message()

        await msg.edit(
            embed=Embed(
                description=f"Toggled maintenance mode {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
        logging.info("Toggled maintenance mode")

    @slash_command(name="purge")
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
        if not await self._has_permissions(ctx, **{"manage_messages": True}):
            return

        # Determine the integer value of count
        if count == "all":
            count = -1
        else:
            try:
                count = int(count)

            # Send error message to the user if unsuccessful
            except ValueError:
                emoji = self.bot.emoji_group.get_emoji("red_cross")
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
        emoji = self.bot.emoji_group.get_emoji("loading_dots")
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
        emoji = self.bot.emoji_group.get_emoji("done")
        await res.edit_original_message(
            embed=Embed(
                description=f"{len(deleted)} message(s) deleted {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @slash_command(name="kick")
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
        if not await self._has_permissions(ctx, **{"kick_members": True}):
            return

        # Kick the member if its not the owner
        if not member == ctx.guild.owner:
            await member.kick(reason=reason)

            # Send log to staff channel
            emoji = self.bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was kicked out by {ctx.author}\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self.bot.STAFF_CHANNEL.send(embed=embed)

        # Show error message if the member to be kicked is th owner
        else:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission error {emoji}",
                    description=f"You can't kick the owner",
                    color=Colors.RED
                ),
                delete_after=3
            )

            # Send log to staff channel
            emoji = self.bot.emoji_group.get_emoji("warning")
            await self.bot.STAFF_CHANNEL.send(
                embed=Embed(
                    title=f"Alert",
                    description=f"{member} tried to kick the owner!",
                    color=Colors.RED
                ).set_thumbnail(url=emoji.url)
            )

    @slash_command(name="ban")
    async def _ban(
            self,
            ctx: ApplicationContext,
            member: Option(Member, "The member to be kicked"),
            reason: Option(str, "Reason for ban") = ""
    ) -> None:
        """
        Ban a memeber from the guild

        Args:
            ctx (ApplicationContext)
            member (Member): Member to be kicked
        """

        # Check for permissions
        if not await self._has_permissions(ctx, **{"ban_members": True}):
            return

        # Ban the member if not owner
        if not member == ctx.guild.owner:
            await member.ban(delete_message_days=0, reason=reason)

            # Send log to the staff channel
            emoji = self.bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was banned by {ctx.author}\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self.bot.STAFF_CHANNEL.send(embed=embed)

        # Otherwise show error message
        else:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission error {emoji}",
                    description=f"You can't ban the owner",
                    color=Colors.RED
                ),
                delete_after=3
            )

            # Send log to staff channel
            emoji = self.bot.emoji_group.get_emoji("warning")
            await self.bot.STAFF_CHANNEL.send(
                embed=Embed(
                    title=f"Alert",
                    description=f"{member} tried to ban the owner!",
                    color=Colors.RED
                ).set_thumbnail(url=emoji.url)
            )

    @slash_command(name="timeout")
    async def _timeout(
            self,
            ctx: ApplicationContext,
            member: Option(Member, "The member to be timed out"),
            duration: Option(int, "Duration in minutes"),
            reason: Option(str, "Reason for timeout") = ""
    ) -> None:
        """
        Timeout a memeber from the guild

        Args:
            ctx (ApplicationContext)
            member (Member): Member to be kicked
        """

        # Check for permissions
        if not await self._has_permissions(ctx, **{"ban_members": True}):
            return

        # Show error message if the user is already timed out
        if member.timed_out:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
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
            emoji = self.bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was timed out by {ctx.author} for "
                            f"{duration} minutes\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self.bot.STAFF_CHANNEL.send(embed=embed)

        # Otherwise show error message
        else:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Permission error {emoji}",
                    description=f"You can't timeout the owner",
                    color=Colors.RED
                ),
                delete_after=3
            )

            # Send log to staff channel
            emoji = self.bot.emoji_group.get_emoji("warning")
            await self.bot.STAFF_CHANNEL.send(
                embed=Embed(
                    title=f"Alert",
                    description=f"{member} tried to timeout the owner!",
                    color=Colors.RED
                ).set_thumbnail(url=emoji.url)
            )

    @slash_command(name="lock")
    async def _lock(self, ctx: ApplicationContext) -> None:
        """
        Lock current channel

        Args:
            ctx (ApplicationContext)
        """

        # Check for permissions
        if not await self._has_permissions(ctx, **{"manage_permissions": 1}):
            return

        # Get the channel from which the command was invoked
        channel: TextChannel = ctx.channel

        # Show error message if already locked
        if not channel.permissions_for(ctx.guild.default_role).send_messages:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
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
        emoji = self.bot.emoji_group.get_emoji("done")
        await ctx.respond(
            embed=Embed(
                description=f"Channel locked {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @slash_command(name="unlock")
    async def _unlock(self, ctx: ApplicationContext) -> None:
        """
        Unlock current channel

        Args:
            ctx (ApplicationContext)
        """

        # Check for permissions
        if not await self._has_permissions(ctx, **{"manage_permissions": 1}):
            return

        # Get the channel from which the command was invoked
        channel: TextChannel = ctx.channel

        # Show error message if already unlocked
        if channel.permissions_for(ctx.guild.default_role).send_messages:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
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
        emoji = self.bot.emoji_group.get_emoji("done")
        await ctx.respond(
            embed=Embed(
                description=f"Channel unlocked {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @slash_command(name="exec")
    async def _exec(self, ctx: ApplicationContext) -> None:
        """
        Execute python code

        Args:
            ctx (ApplicationContext)
        """

        # Check for permissions
        if not await self._has_permissions(ctx, **{"administrator": True}):
            return

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if self._under_maintenance(ctx.channel):
            self.bot.dispatch("maintenance", ctx)
            return

        # Wait for the user to send a codeblock
        try:
            # Send an example
            await ctx.respond(
                embed=Embed(
                    description="Type the code you want to execute"
                                " below inside a codeblock\n\n"
                                "__**Example**__: \n"
                                "\t\`\`\`py\n"
                                "\tYour code here\n"
                                "\t\`\`\`",
                    color=Colors.GOLD
                )
            )

            # Wait for the response
            codeblock: Message = await self.bot.wait_for(
                "message",
                check=lambda msg: (msg.author == ctx.author
                                   and msg.channel == ctx.channel),
                timeout=300.0
            )

        # Show error message if timer exceeds timeout time
        except asyncio.TimeoutError:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.send(
                embed=Embed(
                    description=f"Timeout error {emoji}",
                    color=Colors.RED
                )
            )
            return

        # Show error if its not a valid codeblock
        if not (codeblock.content.startswith("```py")
                and codeblock.content.endswith("```")):

            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.send(
                embed=Embed(
                    description=f"Invalid codeblock {emoji}",
                    color=Colors.RED
                )
            )
            return

        # Prepare the codeblock for execution
        codeblock = codeblock.content.replace("```py", "")
        codeblock = codeblock.replace("```", "")

        # Try to execute the codeblock
        try:
            # Set output stream
            old_stdout = sys.stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout

            # Execute the codeblock
            exec(codeblock)

            # Get output from the new_stdout
            output = new_stdout.getvalue()
            sys.stdout = old_stdout

        # If error occurs, send the error message to the user
        except Exception as e:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.send(
                embed=Embed(
                    title=f"Error executing codeblock {emoji}",
                    description=f"```py\n{e}\n```",
                    color=Colors.RED
                )
            )

        # Send output for successful execution
        else:
            await ctx.send(content=f"{ctx.author.mention}\n"
                           f"```py\n{output}\n```")
