import logging
import asyncio
from datetime import datetime

from discord import (
    ApplicationContext,
    Bot,
    Embed,
    Emoji,
    Game,
    Message,
    Role,
    Status,
    TextChannel,
    Webhook
)

from .utils.color import Colors
from .utils.emoji import EmojiGroup
from .utils.bump_timer import BumpTimer


class ICodeBot(Bot):
    """
    The BOT made for 'iCODE' Discord server.
    """

    def __init__(self, description=None, maintenance=False, *args, **options):
        """
        Instantiate iCODE Bot

        Args:
            description (str, optional): Bot description. Defaults to None.
            maintenance (bool, optional): Whether the bot is under maintenance. Defaults to False.
        """
        super().__init__(description, *args, **options)

        self.MAINTENANCE_MODE = maintenance

    async def on_ready(self) -> None:
        """
        Called when the bot has finished logging in and setting things up
        """

        logging.info(msg=f"Logged in as {self.user}")

        # Create EmojiGroup instance
        logging.info(msg="Initializing EmojiGroup")
        self.emoji_group = EmojiGroup(self)

        # Create BumpTimer instance
        logging.info(msg="Initializing BumpTimer")
        self.bump_timer = BumpTimer()

        # ---
        if self.MAINTENANCE_MODE:
            self.MAINTENANCE_CHANNEL = self.get_channel(955540726513565756)

            await self.change_presence(
                status=Status.do_not_disturb,
                activity=Game(name="| Under Maintenance")
            )
        else:
            # Start timer
            previous_bump_time = self.bump_timer.get_bump_time()
            delta = (datetime.now() - previous_bump_time).total_seconds()

            delay = 0 if delta >= 7200 else (7200 - delta)
            self.dispatch("bump_done", int(delay))

            # Set status
            await self.change_presence(activity=Game(name="/emojis | .py"))

    async def on_bump_done(self, delay: int) -> None:
        """
        Called when a user bumps the server

        Args:
            channel (TextChannel): The channel to which bump reminder 
                                   will be sent
        """
        self.bump_timer.running = True
        await asyncio.sleep(delay=delay)
        self.bump_timer.running = False

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

    async def on_maintenance(self, ctx: ApplicationContext) -> None:
        """
        Called when a member runs a command in maintenance mode

        Args:
            ctx (ApplicationContext)
        """

        emoji: Emoji = self.emoji_group.get_emoji("warning")

        await ctx.respond(
            content=ctx.author.mention,
            embed=Embed(
                title=f"Maintenance Break {emoji}",
                description="iCODE is under maintenance. Commands will work\n"
                            f"only in {self.MAINTENANCE_CHANNEL} channel.",
                color=Colors.GOLD
            ),
            delete_after=5
        )

    async def on_message(self, message: Message) -> None:
        """
        Called when some user sends a messsage in the server

        Args:
            message (Message): Message sent by a user
        """

        # Warn if it's maintenance mode
        if (self.MAINTENANCE_MODE and
                message.channel != self.MAINTENANCE_CHANNEL):
            return

        # Check if it's a Webhook
        if message.webhook_id:
            # Check if the message is from Disboard
            if message.author.id == 302050872383242240:
                if "Bump done" in message.embeds[0].description:
                    self.bump_timer.update_bump_time(datetime.now())
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
