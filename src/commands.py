import asyncio
import logging
from datetime import datetime

from discord import AllowedMentions, Emoji, Interaction, Message
from discord import ApplicationContext, Embed, slash_command
from discord.ext.commands import Cog

from .bot import ICodeBot
from .constants.color import Colors
from .constants.emoji import EmojiGroup
from .utils import get_bump_timestamp


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
        self.BOT = bot

    @slash_command(name="echo")
    async def _echo(self, ctx: ApplicationContext, message: str) -> None:
        """
        Echoes a message

        Args:
            ctx (ApplicationContext)
            message (str): Message sent by some user
        """

        logging.info(f"Echo to {ctx.author.name}")
        await ctx.respond(embed=Embed(title=message, color=Colors.BLUE))

    @slash_command(name="embed")
    async def _embed(self, ctx: ApplicationContext) -> None:
        """
        Command for building embeds

        Args:
            ctx (ApplicationContext)
        """

        def check(message: Message) -> bool:
            return (message.author == ctx.author and
                    message.channel == ctx.channel)

        try:
            res: Interaction = await ctx.respond(
                embed=Embed(title="Embed Title",
                            description="Please provide a title for the embed",
                            color=Colors.BLUE)
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

            if ctx.channel_id == 923530976947224596:
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

        logging.info("Updating server emojis")

        emojis: EmojiGroup = self.BOT.emoji_group
        res: Interaction = await ctx.respond(
            embed=Embed(
                title=f"Updating emojis {emojis.get_emoji('loading_dots')}",
                color=Colors.GOLD
            )
        )
        res_msg: Message = await res.original_message()

        self.BOT.emoji_group.update_emojis()

        await res_msg.edit(
            embed=Embed(
                title=f"Emojis updated {emojis.get_emoji('done')}",
                color=Colors.GREEN
            )
        )
        await res_msg.delete(delay=2)

    @slash_command(name="emojis")
    async def _list_emojis(self, ctx: ApplicationContext) -> None:
        """
        List available emojis

        Args:
            ctx (ApplicationContext)
        """

        embed = Embed(
            title="Server Emojis",
            description="Everyone can use below listed emojis!",
            timestamp=datetime.now(),
            color=Colors.GOLD
        )

        emoji_group = self.BOT.emojis
        emojis = [f"{emoji} • `:{emoji.name}:`"
                  for emoji in emoji_group if not emoji.animated]

        embed = embed.add_field(name="Normal Emojis", value="\n".join(emojis))

        emojis = [f"{emoji} • `:{emoji.name}:`"
                  for emoji in emoji_group if emoji.animated]

        embed = embed.add_field(name="Animated Emojis",
                                value="\n".join(emojis))

        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        embed.set_thumbnail(
            url="https://emoji.gg/assets/emoji/1030-stand-with-ukraine.png")

        await ctx.respond(embed=embed)

    @slash_command(name="update-bump-timer")
    async def _update_reminder(self, ctx: ApplicationContext) -> None:
        """
        Fix error in bump timer

        Args:
            ctx (ApplicationContext)    
        """

        emojis: EmojiGroup = self.BOT.emoji_group
        emoji: Emoji = emojis.get_emoji('loading_gears')

        res: Interaction = await ctx.respond(
            embed=Embed(
                title=f"Updating bump timer {emoji}",
                color=Colors.GOLD
            )
        )
        msg: Message = await res.original_message()

        if self.BOT.bump_timer_on:
            emoji = emojis.get_emoji("red_cross")
            
            await msg.edit(
                embed=Embed(
                    title=f"Error updating bump timer {emoji}",
                    description="Bump timer is already running",
                    color=Colors.RED
                )
            )
            
            await msg.delete(delay=2)
            return

        previous_bump_time = get_bump_timestamp()
        delta = (datetime.now() - previous_bump_time).seconds

        delay = 0 if delta >= 60 else (60 - delta)
        self.BOT.dispatch("bump_done", delay)

        emoji = emojis.get_emoji("done")
        await msg.edit(
            embed=Embed(
                title=f"Bump reminder updated {emoji}",
                color=Colors.GREEN
            )
        )
        await msg.delete(delay=2)
