import sys
import asyncio
import logging
from io import StringIO

from discord import (
    Cog,
    Game,
    Embed,
    Status,
    Message,
    Interaction,
    ApplicationContext
)
from discord.ext.commands import (
    slash_command
)


from ..bot import ICodeBot
from ..utils.color import Colors
from ..utils.checks import (
    maintenance_check,
    permission_check
)


class MiscellaneousCommands(Cog):
    """
    Miscellaneous commands    
    """

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @slash_command(name="toggle-maintenance-mode")
    @permission_check(bot_owner=True)
    async def _toggle_maintenance_mode(self, ctx: ApplicationContext) -> None:
        """
        Turn maintenance mode on or off

        Args:
            ctx (ApplicationContext)
        """

        # Respond with an embed and toggle maintenance mode
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        if self._bot.MAINTENANCE_MODE:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    description=f"Disabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self._bot.change_presence(activity=Game(name="/emojis | .py"))

        else:
            res: Interaction = await ctx.respond(
                embed=Embed(
                    description=f"Enabling maintenance mode {emoji}",
                    color=Colors.GOLD,
                )
            )

            # Change presence
            await self._bot.change_presence(
                status=Status.do_not_disturb,
                activity=Game(name="| Under Maintenance")
            )

        # Toggle maintenance mode
        self._bot.MAINTENANCE_MODE = not self._bot.MAINTENANCE_MODE
        await asyncio.sleep(1)

        # Prompt completion
        emoji = self._bot.emoji_group.get_emoji("done", ctx.guild.id)
        msg: Message = await res.original_message()

        await msg.edit(
            embed=Embed(
                description=f"Toggled maintenance mode {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
        logging.info("Toggled maintenance mode")

    @slash_command(name="exec")
    @maintenance_check()
    @permission_check(bot_owner=True)
    async def _exec(self, ctx: ApplicationContext) -> None:
        """
        Execute python code

        Args:
            ctx (ApplicationContext)
        """

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
            codeblock: Message = await self._bot.wait_for(
                "message",
                check=lambda msg: (msg.author == ctx.author
                                   and msg.channel == ctx.channel),
                timeout=300.0
            )

        # Show error message if timer exceeds timeout time
        except asyncio.TimeoutError:
            emoji = self._bot.emoji_group.get_emoji("red_cross", ctx.guild.id)
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

            emoji = self._bot.emoji_group.get_emoji("red_cross", ctx.guild.id)
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
            emoji = self._bot.emoji_group.get_emoji("red_cross", ctx.guild.id)
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
