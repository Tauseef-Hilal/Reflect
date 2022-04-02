import asyncio
import logging
from io import StringIO
from datetime import datetime, timedelta
import sys

from discord import (
    AllowedMentions,
    ButtonStyle,
    Game,
    Interaction,
    Member,
    Message,
    ApplicationContext,
    Embed,
    Permissions,
    Role,
    Status,
    TextChannel
)
from discord.ext.commands import (
    Cog,
    slash_command
)
from discord.ui import (
    View,
    Button,
    button
)


from .bot import ICodeBot
from .utils.color import Colors
from .utils.emoji import EmojiGroup
from .utils.constants import ANNOUNCEMENTS_CHANNEL_ID, BUMPER_ROLE_ID


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
            channel (TextChannel): The channel from which a cmd was run

        Returns:
            bool: True if under maintenance
        """

        return (self.bot.MAINTENANCE_MODE and
                channel != self.bot.MAINTENANCE_CHANNEL)

    async def _has_permissions(self, ctx: ApplicationContext, **perms) -> bool:
        """
        Check whether a member has required permissions to
        run a specific command

        Returns:
            bool: True if the member has all of the perms
        """

        channel: TextChannel = ctx.channel
        permissions: Permissions = channel.permissions_for(ctx.author)

        missing = [perm for perm, value in perms.items()
                   if getattr(permissions, perm) != value]

        if not missing:
            return True

        # Show error message to the member
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

    @slash_command(name="echo")
    async def _echo(self, ctx: ApplicationContext, message: str) -> None:
        """
        Echoes a message

        Args:
            ctx (ApplicationContext)
            message (str): Message sent by some user
        """

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if self._under_maintenance(ctx.channel):
            self.bot.dispatch("maintenance", ctx)
            return

        await ctx.respond(embed=Embed(description=message, color=Colors.BLUE))

    @slash_command(name="embed")
    async def _embed(self, ctx: ApplicationContext) -> None:
        """
        Command for building embeds

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
        count: str,
        from_user: Member = None
    ) -> None:
        """
        Delete a specified number of messages

        Args:
            ctx (ApplicationContext):
            count (MessageCountConverter): Number of messages to delete
        """

        # Check
        if not await self._has_permissions(ctx, **{"manage_messages": True}):
            return

        if count == "all":
            count = -1
        else:
            try:
                count = int(count)
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

        emoji = self.bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Fetching messages {emoji}",
                color=Colors.GOLD
            )
        )

        channel: TextChannel = ctx.channel
        limit = None if count == -1 else count + 1

        if from_user:
            counter = 0
            messages = []
            async for msg in channel.history(limit=None):
                if msg.author == from_user or counter == 0:
                    messages.append(msg)
                    counter += 1

                if counter == limit:
                    break
        else:
            messages = await channel.history(limit=limit).flatten()

        await res.edit_original_message(
            embed=Embed(
                description=f"Deleting {len(messages) - 1} messages {emoji}",
                color=Colors.GOLD
            )
        )

        for msg in messages[1:]:
            await msg.delete()

        emoji = self.bot.emoji_group.get_emoji("done")
        await res.edit_original_message(
            embed=Embed(
                description=f"Messages deleted {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @slash_command(name="kick")
    async def _kick(
            self,
            ctx: ApplicationContext,
            member: Member,
            reason: str = ""
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

        if not member == ctx.guild.owner:
            await member.kick(reason=reason)

            emoji = self.bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was kicked out by {ctx.author}\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self.bot.STAFF_CHANNEL.send(embed=embed)
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
            member: Member,
            reason: str = ""
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

        if not member == ctx.guild.owner:
            await member.ban(delete_message_days=0, reason=reason)

            emoji = self.bot.emoji_group.get_emoji("rules")
            embed = Embed(
                title=f"Moderation log",
                description=f"{member} was banned by {ctx.author}\n"
                            f"Reason: {reason if reason else 'None provided'}",
                color=Colors.RED
            ).set_thumbnail(url=emoji.url)

            await ctx.respond(embed=embed, delete_after=4)
            await self.bot.STAFF_CHANNEL.send(embed=embed)
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
            member: Member,
            duration: int,
            reason: str = ""
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

        if member.timed_out:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.respond(
                embed=Embed(
                    title=f"Command error {emoji}",
                    description="The member is already timed out"
                )
            )
            return

        if not member == ctx.guild.owner:
            await member.timeout_for(
                duration=timedelta(minutes=duration),
                reason=reason
            )

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

        channel: TextChannel = ctx.channel
        bumper: Role = self.bot.GUILD.get_role(BUMPER_ROLE_ID)

        if not channel.permissions_for(bumper).send_messages:
            await ctx.respond(
                embed=Embed(
                    description="Channel is already locked",
                    color=Colors.RED
                ),
                delete_after=2
            )
            return

        await channel.set_permissions(
            target=bumper,
            send_messages=False
        )

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

        channel: TextChannel = ctx.channel
        bumper: Role = self.bot.GUILD.get_role(BUMPER_ROLE_ID)

        if channel.permissions_for(bumper).send_messages:
            await ctx.respond(
                embed=Embed(
                    description="Channel is already unlocked",
                    color=Colors.RED
                ),
                delete_after=2
            )
            return

        await channel.set_permissions(
            target=bumper,
            send_messages=True
        )

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

        def check(message: Message) -> bool:
            return (message.author == ctx.author and
                    message.channel == ctx.channel)

        try:
            res: Interaction = await ctx.respond(
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

            codeblock: Message = await self.bot.wait_for("message",
                                                         check=check,
                                                         timeout=300.0)

        except asyncio.TimeoutError:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.send(
                embed=Embed(
                    description=f"Timeout error {emoji}",
                    color=Colors.RED
                )
            )
            return

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

        codeblock = codeblock.content.replace("```py", "")
        codeblock = codeblock.replace("```", "")

        try:
            old_stdout = sys.stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout

            output = exec(codeblock)
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
        except Exception as e:
            emoji = self.bot.emoji_group.get_emoji("red_cross")
            await ctx.send(
                embed=Embed(
                    title=f"Error executing codeblock {emoji}",
                    description=f"```py\n{e}\n```",
                    color=Colors.RED
                )
            )
        else:
            await ctx.send(content=f"```py\n{output}\n```")
   
    # @slash_command(name="trivia")
    # async def _trivia(self, ctx: ApplicationContext) -> None:
    #     """
    #     Get a random question

    #     Args:
    #         ctx (ApplicationContext)
    #     """
    #     options = ["create [5]",
    #                "list(5)",
    #                "[1] * 5",
    #                "None of these"]
    #     answer = "[1] * 5"

    #     await ctx.respond(
    #         embed=Embed(
    #             title="Here is a challenge!",
    #             description="Which of the following creates a list with 5 items?",
    #             color=Colors.BLUE
    #         ),
    #         view=Options(ctx.channel, self.bot, options, answer)
    #     )


# class Option(Button):

#     def __init__(self, parent: View, bot: ICodeBot, answer: str, **kwargs):
#         """
#         Initialize a button

#         Args:
#             answer (str): The answer to the question
#         """
#         super().__init__(**kwargs)

#         self.parent = parent
#         self.bot = bot
#         self.answer = answer

#     async def callback(self, interaction: Interaction) -> None:
#         """
#         On clicking the option

#         Args:
#             interaction (Interaction)
#         """

#         if self.label == self.answer:
#             self.style = ButtonStyle.success

#             emoji = self.bot.emoji_group.get_emoji("done")
#             embed = Embed(
#                 title=f"Good Job {emoji}",
#                 description=f"The answer is `{self.answer}`",
#                 color=Colors.GREEN
#             )
#         else:
#             self.style = ButtonStyle.danger

#             emoji = self.bot.emoji_group.get_emoji("red_cross")
#             embed = Embed(
#                 title=f"Thats a shame {emoji}",
#                 description=f"The answer is `{self.answer}`",
#                 color=Colors.RED
#             )

#         for child in self.parent.children:
#             child.disabled = True

#         await interaction.response.edit_message(view=self.parent)

#         channel = interaction.channel
#         await channel.send(embed=embed)


# class Options(View):

#     def __init__(
#         self,
#         channel: TextChannel,
#         bot: ICodeBot,
#         options: list,
#         answer: str
#     ) -> None:
#         """
#         Create buttons for different options

#         Args:
#             channel (TextChannel): The calling channel
#             bot (ICodeBot): Discord bot
#             options (list): Options for the questions
#             answer (str): Questions answer
#         """
#         super().__init__(timeout=30)
#         self.channel = channel

#         # Create options
#         for i in range(1, 5):
#             btn = Option(
#                 parent=self,
#                 bot=bot,
#                 answer=answer,
#                 label=options.pop(),
#                 style=ButtonStyle.primary,
#                 row=i
#             )
#             self.add_item(btn)

#     async def on_timeout(self) -> None:
#         """
#         Handle timeout event
#         """

#         pass
