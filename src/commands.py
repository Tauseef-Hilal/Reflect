import asyncio
import logging
from datetime import datetime

from discord import AllowedMentions, Interaction, Message, Bot
from discord import ApplicationContext, Embed, slash_command
from discord.ext.commands import Cog

from .constants.color import Colors


class CommandGroup(Cog):
    """
    Group of slash commands
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self.BOT = bot

    @slash_command()
    async def echo(self, ctx: ApplicationContext, message: str) -> None:
        """
        Echoes a message

        Args:
            ctx (ApplicationContext)
            message (str): Message sent by some user
        """

        logging.info(f"Echo to {ctx.author.name}")
        await ctx.respond(embed=Embed(title=message, color=Colors.BLUE))

    @slash_command()
    async def embed(self, ctx: ApplicationContext) -> None:
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
