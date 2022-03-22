import logging

import discord


class ICodeBot(discord.Bot):
    """
    The BOT made for 'iCODE' Discord server.
    """

    async def on_ready(self) -> None:
        """
        Called when the bot has finished logging in and setting things up 
        """

        logging.info(msg=f"Logged in as {self.user}")
