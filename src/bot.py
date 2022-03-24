import logging
import asyncio
import datetime

from discord import Activity, Bot, Embed, Emoji, Game, Message, Role, TextChannel, Webhook

from .constants.emoji import EmojiGroup
from .constants.color import Colors
from .utils import update_bump_timestamp


class ICodeBot(Bot):
    """
    The BOT made for 'iCODE' Discord server.
    """
    emoji_group: EmojiGroup
    bump_timer_on = False

    async def on_ready(self) -> None:
        """
        Called when the bot has finished logging in and setting things up
        """

        logging.info(msg=f"Logged in as {self.user}")

        # Create constants.emoji.EmojiGroup instance
        logging.info(msg="Initializing EmojiGroup")
        self.emoji_group = EmojiGroup(self)
        
        await self.change_presence(activity=Game(name="Discord.PY"))

    async def on_bump_done(self, delay: int) -> None:
        """
        Called when a user bumps the server

        Args:
            channel (TextChannel): The channel to which bump reminder 
                                   will be sent
        """
        self.bump_timer_on = True
        await asyncio.sleep(delay=delay)
        self.bump_timer_on = False

        channel: TextChannel = self.get_channel(923529458508529674)
        bumper: Role = channel.guild.get_role(956603384968925245)
        reminder: Emoji = self.emoji_group.get_emoji("reminder")

        await channel.send(
            content=f"{bumper.mention}",
            embed=Embed(
                title=f"Bump Reminder {reminder}",
                description="Help grow this server. Run `/bump`",
                color=Colors.GOLD
            )
        )

    async def on_message(self, message: Message) -> None:
        """
        Called when some user sends a messsage in the server

        Args:
            message (Message): Message sent by a user
        """

        # Check if it's a Webhook
        if message.webhook_id:
            # Check if the message is from Disboard
            if message.author.id == 302050872383242240:
                if "Bump done" in message.embeds[0].description:
                    update_bump_timestamp(datetime.datetime.now())
                    self.dispatch("bump_done", 7200)
            return

        # AEWN: Animated Emojis Without Nitro
        if message.content.count(":") > 1:
            await self._animated_emojis(message)

    async def _animated_emojis(self, message: Message) -> None:
        """
        Animated Emojis Without Nitro

        Args:
            message (Message): Message with emojis
        """

        emoji = None
        temp = []
        for word in message.content.split():
            if word[0] == word[-1] == ":" and len(word) > 2 and word not in temp:

                try:
                    emoji: Emoji = self.emoji_group.get_emoji(word[1:-1])

                    message.content = message.content.replace(word, str(emoji))
                    temp.append(word)

                except AttributeError:
                    pass

        if emoji:
            webhooks = await message.channel.webhooks()

            webhook: Webhook
            for webhook in webhooks:
                if webhook.user.id == self.user.id:
                    break
            else:
                avatar: bytes = await message.author.display_avatar.read()

                webhook: Webhook = await message.channel.create_webhook(
                    name="iCODE-BOT",
                    avatar=avatar,
                    reason="Animated Emoji Usage"
                )

            await webhook.send(content=message.content,
                               username=message.author.display_name, avatar_url=message.author.display_avatar)
            await message.delete()
