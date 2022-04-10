import asyncio
import logging
from datetime import (
    datetime,
)

from discord import (
    Embed,
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


from ..bot import ICodeBot
from ..utils.color import Colors
from ..utils.emoji import EmojiGroup
from ..utils.constants import ANNOUNCEMENTS_CHANNEL_ID


def under_maintenance(bot, ctx: ApplicationContext) -> bool:
    """
    Check if the bot is under maintenance

    Args:
        `channel` (TextChannel): The channel from which a cmd was run

    Returns:
        bool: True if under maintenance
    """

    if (bot.MAINTENANCE_MODE
            and ctx.channel != bot.MAINTENANCE_CHANNEL):
        bot.dispatch("maintenance", ctx)
        return True
    return False


async def has_permissions(
        bot: ICodeBot,
        ctx: ApplicationContext,
        **perms) -> bool:
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
    emoji = bot.emoji_group.get_emoji("red_cross")
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


class GeneralCommands(Cog):
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
        self._bot = bot

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
        if under_maintenance(self._bot, ctx):
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
    async def _update_emojis(self, ctx: ApplicationContext) -> None:
        """
        Update server emojis. Run this command after adding new emojis

        Args:
            ctx (ApplicationContext)
        """

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if under_maintenance(self._bot, ctx):
            return

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

    @slash_command(name="emojis")
    async def _list_emojis(self, ctx: ApplicationContext) -> None:
        """
        List available emojis

        Args:
            ctx (ApplicationContext)
        """

        # Fire maintenance event if under maintenance
        # and ctx.channel is not maintenance channel
        if under_maintenance(self._bot, ctx):
            return

        # Create embed
        embed = Embed(
            title="Server Emojis",
            description="Everyone can use below listed emojis!",
            timestamp=datetime.now(),
            color=Colors.GOLD
        )

        # Add normal emojis to the embed
        emoji_group = self._bot.emojis
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
        embed.set_thumbnail(url=self._bot.emoji_group.get_emoji("ukraine").url)

        # Send embed
        await ctx.respond(embed=embed)
