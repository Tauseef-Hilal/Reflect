import asyncio
import logging
from datetime import datetime

from discord import (
    AllowedMentions,
    Game,
    Interaction,
    Message,
    ApplicationContext,
    Embed,
    Status,
    TextChannel,
    slash_command
)
from discord.ext import commands


from .bot import ICodeBot
from .utils.color import Colors
from .utils.emoji import EmojiGroup
from .utils.constants import ANNOUNCEMENTS_CHANNEL_ID


class CommandGroup(commands.Cog):
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
        self.BOT = bot

    def _under_maintenance(self, channel: TextChannel) -> bool:
        """
        Check if the bot is under maintenance

        Args:
            channel (TextChannel): The channel from which a cmd was run

        Returns:
            bool: True if under maintenance
        """

        return (self.BOT.MAINTENANCE_MODE and
                channel != self.BOT.MAINTENANCE_CHANNEL)

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
            self.BOT.dispatch("maintenance", ctx)
            return

        await ctx.respond(embed=Embed(title=message, color=Colors.BLUE))

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
            self.BOT.dispatch("maintenance", ctx)
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

            title: Message = await self.BOT.wait_for("message",
                                                     check=check,
                                                     timeout=60.0)

            msg2: Message = await ctx.send(
                embed=Embed(
                    title="Embed Description",
                    description="Please provide a description for the embed",
                    color=Colors.BLUE)
            )
            desc: Message = await self.BOT.wait_for("message",
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
                                         icon_url=self.BOT.user.avatar)

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
            self.BOT.dispatch("maintenance", ctx)
            return

        logging.info("Updating server emojis")

        # Send `loading` embed
        emojis: EmojiGroup = self.BOT.emoji_group
        res: Interaction = await ctx.respond(
            embed=Embed(
                title=f"Updating emojis {emojis.get_emoji('loading_dots')}",
                color=Colors.GOLD
            )
        )
        res_msg: Message = await res.original_message()

        # Update emoji_group
        self.BOT.emoji_group.update_emojis()

        # For fun
        await asyncio.sleep(1)

        # Send `done` embed
        await res_msg.edit(
            embed=Embed(
                title=f"Emojis updated {emojis.get_emoji('done')}",
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
            self.BOT.dispatch("maintenance", ctx)
            return

        # Create embed
        embed = Embed(
            title="Server Emojis",
            description="Everyone can use below listed emojis!",
            timestamp=datetime.now(),
            color=Colors.GOLD
        )

        # Add normal emojis to the embed
        emoji_group = self.BOT.emojis
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
        embed.set_thumbnail(url=self.BOT.emoji_group.get_emoji("ukraine").url)

        # Send embed
        await ctx.respond(embed=embed)

    @slash_command(name="toggle-maintenance-mode")
    @commands.is_owner()
    async def _toggle_maintenance_mode(self, ctx: ApplicationContext) -> None:
        """
        Turn maintenance mode on or off

        Args:
            ctx (ApplicationContext)
        """

        emoji = self.BOT.emoji_group.get_emoji("loading_dots")

        # Respond with an embed and toggle maintenance mode
        if self.BOT.MAINTENANCE_MODE:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    title=f"Disabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self.BOT.change_presence(activity=Game(name="/emojis | .py"))

        else:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    title=f"Enabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self.BOT.change_presence(
                status=Status.do_not_disturb,
                activity=Game(name="| Under Maintenance")
            )

        # Toggle maintenance mode
        self.BOT.MAINTENANCE_MODE = not self.BOT.MAINTENANCE_MODE
        await asyncio.sleep(1)

        # Prompt completion
        emoji = self.BOT.emoji_group.get_emoji("done")
        msg: Message = await res.original_message()

        await msg.edit(
            embed=Embed(
                title=f"Toggled maintenance mode {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @_toggle_maintenance_mode.error
    async def _toggle_maintenance_mode_error(
        self,
        ctx: commands.Context,
        error: commands.CommandError
    ) -> None:
        """
        Handle error in toggle-maintenance-mode cmd

        Args:
            ctx (commands.Context)
            error (commands.CommandError)
        """

        emoji = self.BOT.emoji_group.get_emoji("red_cross")

        if isinstance(error, commands.NotOwner):
            embed = Embed(
                title=f"Permission Error {emoji}",
                description="You don't have the permission"
                            " to run this command",
                color=Colors.RED
            )
        else:
            logging.error(error)
            embed = Embed(
                title=f"Internal Error {emoji}",
                color=Colors.RED
            )

        await ctx.respond(embed=embed, delete_after=3)
