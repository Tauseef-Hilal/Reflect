import asyncio
import logging
from random import choice
from datetime import datetime
from re import (
    DOTALL,
    findall
)

from pymongo.collection import Collection
from discord import (
    Bot,
    Game,
    Role,
    Embed,
    Emoji,
    Member,
    Status,
    Message,
    Webhook,
    TextChannel,
    PartialEmoji,
    ApplicationContext,
    RawReactionActionEvent,
)

from .utils.db import get_database
from .utils.youtube import YouTube
from .utils.filter import Filter
from .utils.color import Colors
from .utils.emoji import EmojiGroup
from .utils.bump_timer import BumpTimer
from .utils.env import (
    ICODE_GUILD_ID,
    MONGO_DB_URI
)
from .utils.constants import (
    CPP_ROLE_ID,
    RUBY_ROLE_ID,
    JAVA_ROLE_ID,
    DART_ROLE_ID,
    CLANG_ROLE_ID,
    PYTHON_ROLE_ID,
    CSHARP_ROLE_ID,
    CLOJURE_ROLE_ID,
    BUMPER_ROLE_ID,
    ICODIAN_ROLE_ID,
    JAVASCRIPT_ROLE_ID,
    STAFF_CHANNEL_ID,
    TYPESCRIPT_ROLE_ID,
    WELCOME_MESSAGES,
    FAREWELL_MESSAGES,
    SELF_ROLES_CHANNEL_ID,
    MAINTENANCE_CHANNEL_ID,
    INTRODUCTION_CHANNEL_ID,
    GENERAL_CHAT_CHANNEL_ID,
    SERVER_RULES_CHANNEL_ID,
    DISBOARD_ID,
)


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

        # Create Filter instance
        logging.info(msg="Initializing Filter")
        self.filter = Filter()

        # Create YouTube instance
        logging.info("Initializing YouTube API")
        self.youtube = YouTube()

        # Get database
        logging.info("Getting database")
        self.db = get_database(MONGO_DB_URI)

        # Create BumpTimer instance
        logging.info(msg="Initializing BumpTimer")
        self.bump_timer = BumpTimer()

        # Set up reaction roles
        logging.info("Setting up reaction roles")

        self.ICODE_GUILD = self.get_guild(ICODE_GUILD_ID)
        if not self.ICODE_GUILD:
            logging.warning("Couldn't find iCODE")

        self.REACTION_ROLES = {
            "cpp": self.ICODE_GUILD.get_role(CPP_ROLE_ID),
            "java": self.ICODE_GUILD.get_role(JAVA_ROLE_ID),
            "ruby": self.ICODE_GUILD.get_role(RUBY_ROLE_ID),
            "clang": self.ICODE_GUILD.get_role(CLANG_ROLE_ID),
            "python": self.ICODE_GUILD.get_role(PYTHON_ROLE_ID),
            "csharp": self.ICODE_GUILD.get_role(CSHARP_ROLE_ID),
            "dartlang": self.ICODE_GUILD.get_role(DART_ROLE_ID),
            "ukraine": self.ICODE_GUILD.get_role(BUMPER_ROLE_ID),
            "clojure": self.ICODE_GUILD.get_role(CLOJURE_ROLE_ID),
            "javascript": self.ICODE_GUILD.get_role(JAVASCRIPT_ROLE_ID),
            "typescript": self.ICODE_GUILD.get_role(TYPESCRIPT_ROLE_ID)
        }

        # Start bump timer
        for collection_name in self.db.list_collection_names():
            collection = self.db.get_collection(collection_name)

            logging.info(f"Getting previous bump time for {collection_name}")

            try:
                previous_bump_time = self.bump_timer.get_bump_time(collection)
            except (TypeError, KeyError):
                logging.warning("No bump data found")
                continue

            logging.info(f"Previous bump time: {previous_bump_time}")

            delta = (datetime.now() - previous_bump_time).total_seconds()
            delay = 0 if delta >= 7200 else (7200 - delta)

            self.dispatch("bump_done", collection, int(delay))

        # Set maintenance and staff channel
        self.MAINTENANCE_CHANNEL = self.get_channel(MAINTENANCE_CHANNEL_ID)
        self.STAFF_CHANNEL = self.get_channel(STAFF_CHANNEL_ID)

        # Set DND if the bot is running in maintenance mode,
        if self.MAINTENANCE_MODE:
            await self.change_presence(
                status=Status.do_not_disturb,
                activity=Game(name="| Under Maintenance")
            )

        # Otherwise
        else:
            # Set Online (activity)
            await self.change_presence(activity=Game(name="UMF 2022"))

    async def on_maintenance(self, ctx: ApplicationContext) -> None:
        """
        Called when a member runs a command in maintenance mode

        Args:
            ctx (ApplicationContext)
        """

        # Get `warning` emoji
        emoji: Emoji = self.emoji_group.get_emoji("warning")

        # Send embed to maintenance channel
        await ctx.respond(
            content=ctx.author.mention,
            embed=Embed(
                title=f"Maintenance Break {emoji}",
                description="iCODE is under maintenance. Commands will work\n"
                            f"only in the {self.MAINTENANCE_CHANNEL} channel "
                            "of iCODE server.",
                color=Colors.GOLD
            ),
            delete_after=5
        )

    async def on_raw_reaction_add(
            self,
            payload: RawReactionActionEvent
    ) -> None:
        """
        Called when a user reacts to some msg

        Args:
            payload (RawReactionActionEvent)
        """

        if payload.message_id == 957283616541536317:
            emoji: PartialEmoji = payload.emoji

            try:
                role: Role = self.REACTION_ROLES[emoji.name]
            except KeyError:
                pass
            else:
                await payload.member.add_roles(role)
                logging.info(f"Added {role} role to {payload.member}")

    async def on_raw_reaction_remove(
        self,
        payload: RawReactionActionEvent
    ) -> None:
        """
        Called when a user removes a reaction from some msg

        Args:
            payload (RawReactionActionEvent)
        """

        if payload.message_id == 957283616541536317:
            emoji: PartialEmoji = payload.emoji

            try:
                role: Role = self.REACTION_ROLES[emoji.name]
            except KeyError:
                pass
            else:
                member: Member = await self.ICODE_GUILD \
                    .fetch_member(payload.user_id)

                if member:
                    await member.remove_roles(role)
                    logging.info(f"Removed {role} role from {member}")

    async def on_member_join(self, member: Member) -> None:
        """
        Called when a new member joins

        Args:
            member (Member): New member
        """

        # Set up required channels
        try:
            collection = self.db.get_collection(str(member.guild.id))
            console = self.get_channel(
                collection.find_one()["channel_ids"]["console_channel"]
            )
            assert isinstance(console, TextChannel)
        except (KeyError, TypeError, AssertionError):
            return

        # Send embed with random welcome msg to console channel
        await console.send(
            embed=Embed(
                description=choice(
                    WELCOME_MESSAGES
                ).format(
                    member.display_name
                ),
                color=Colors.GREEN
            )
        )

        if member.guild.id != ICODE_GUILD_ID:
            return

        g_chat_channel: TextChannel = self.get_channel(GENERAL_CHAT_CHANNEL_ID)
        intro_channel: TextChannel = self.get_channel(INTRODUCTION_CHANNEL_ID)
        rules_channel: TextChannel = self.get_channel(SERVER_RULES_CHANNEL_ID)
        roles_channel: TextChannel = self.get_channel(SELF_ROLES_CHANNEL_ID)

        # Give iCodian role to member
        role: Role = member.guild.get_role(ICODIAN_ROLE_ID)
        await member.add_roles(role)

        # Send embed to general-chat channel
        await g_chat_channel.send(
            content=member.mention,
            embed=Embed(
                title=f"Welcome to the server {member.display_name}!",
                description="Glad to have you here. "
                            "Have a look around the server.\n\n"
                            f"Introduce yourself in {intro_channel.mention}\n"
                            f"Read server rules in   {rules_channel.mention}\n"
                            f"Get self roles from     {roles_channel.mention}",
                color=Colors.GOLD,
                timestamp=datetime.now()
            ).set_thumbnail(
                url=member.display_avatar
            ).set_footer(
                text=f"{self.user.display_name} Staff",
                icon_url=self.user.display_avatar
            )
        )

    async def on_member_remove(self, member: Member) -> None:
        """
        Called when a member leaves the server

        Args:
            member (Member): Leaving member
        """

        # Set up required channels
        try:
            collection = self.db.get_collection(str(member.guild.id))
            console = self.get_channel(
                collection.find_one()["channel_ids"]["console_channel"]
            )
            assert isinstance(console, TextChannel)
        except (KeyError, TypeError, AssertionError):
            logging.warn("Console channel not set")
            return

        # Send embed with random farewell msg to receiver channel
        await console.send(
            embed=Embed(
                description=choice(
                    FAREWELL_MESSAGES
                ).format(
                    member.display_name
                ),
                color=Colors.RED
            )
        )

    async def on_bump_done(self, collection: Collection, delay: int) -> None:
        """
        Called when a user bumps the server

        Args:
            channel (TextChannel): The channel to which bump reminder
                                   will be sent
        """

        # Sleep for `delay` number of seconds
        logging.info(f"Setting timer for {delay} second(s)")

        await asyncio.sleep(delay=delay)
        logging.info("Timer complete")

        # Get ids
        bumper = None
        try:
            # Set up receiver channel
            channel_ids = collection.find_one()["channel_ids"]
            channel = self.get_channel(
                channel_ids["bump_reminder_channel"]
            )
            assert isinstance(channel, TextChannel)

            # Get bumper role
            role_ids = collection.find_one()["role_ids"]
            bumper = channel.guild.get_role(
                role_ids["server_bumper_role"]
            )
            assert isinstance(bumper, Role)
        except (KeyError, TypeError, AssertionError):
            logging.warning("Reminder channel or bumper role not set")

            if not channel:
                emoji = self.emoji_group.get_emoji("warning")
                for channel in self.get_guild(int(collection.name)).text_channels:
                    if channel.can_send(Embed(title="1")):
                        break

                await channel.send(
                    embed=Embed(
                        description=f"{emoji} I defaulted the reminder to "
                                    "this channel cause it's not set up. "
                                    "Please setup the bump timer first "
                                    "using `/setup` command.",
                        color=Colors.RED
                    )
                )
                return

        # Get `reminder` emoji
        reminder: Emoji = self.emoji_group.get_emoji("reminder")

        # Send embed to the receiver channel
        logging.info(f"Sending reminder to {channel} channel")

        await channel.send(
            content=f"{bumper.mention if bumper else 'NO ROLE'}",
            embed=Embed(
                title=f"Bump Reminder {reminder}",
                description="Help grow this server. Run `/bump`",
                color=Colors.GOLD
            )
        )

    async def on_message_delete(self, message: Message) -> None:
        """
        Called when a message gets deleted

        Args:
            message (Message): The deleted message
        """
        # Return if its iCODE's msg
        if message.author == self.user:
            return

        # Get staff channel
        try:
            collection = self.db.get_collection(str(message.guild.id))
            channel = self.get_channel(
                collection.find_one()["channel_ids"]["modlogs_channel"]
            )
        except KeyError:
            return

        embeds = message.embeds
        embeds.insert(
            0,
            Embed(
                color=Colors.RED,
                timestamp=datetime.now()
            ).set_author(
                name=(f"{message.author.display_name}'s "
                      "message was deleted"),
                icon_url=message.author.display_avatar
            )
            .set_footer(
                text="Message embeds are listed below",
                icon_url=self.user.display_avatar
            ).add_field(
                name="Message Content",
                value=message.content if message.content else "[No content]",
                inline=False
            ).add_field(
                name="Attachments",
                value="\n".join(
                    [f"[{attachment.filename}]({attachment.url})"
                     for attachment in message.attachments]
                )
            )
        )

        # Send msg to staff channel
        await channel.send(
            embeds=embeds,

        )

    async def on_message(self, message: Message) -> None:
        """
        Called when some user sends a messsage in the server

        Args:
            message (Message): Message sent by a user
        """

        # Update bump timer
        if message.author.id == DISBOARD_ID:
            if "Bump done" in message.embeds[0].description:
                logging.info("Updating bump time")
                collection = self.db.get_collection(str(message.guild.id))

                try:
                    self.bump_timer.update_bump_time(
                        collection, datetime.now()
                    )
                except TypeError:
                    logging.warning("Cant update bump time")

                    emoji = self.emoji_group.get_emoji("red_cross")
                    await message.channel.send(
                        embed=Embed(
                            description=f"{emoji} Cannot set bump reminder. "
                                        "Please setup bump reminder first " "using `/setup` command",
                            color=Colors.RED
                        ),
                        delete_after=5
                    )
                else:
                    self.dispatch("bump_done", collection, 7200)
            return

        # AEWN: Animated Emojis Without Nitro
        if message.content.count(":") > 1 and not message.webhook_id:
            await self._animated_emojis(message)

        # Check for profanity words
        if self.filter.has_abusive_words(message.content):
            message.content = self.filter.censor(message.content)
            await self._send_webhook(message=message)
            await message.delete()

    async def _animated_emojis(self, message: Message) -> None:
        """
        Animated Emojis Without Nitro

        Args:
            message (Message): Message with emojis
        """

        emoji = None
        temp = []

        # Return if under maintenance
        if (self.MAINTENANCE_MODE and
                message.channel != self.MAINTENANCE_CHANNEL):
            return

        # Check if an unanimated emoji was sent alone
        # or the author of the message is a nitro user
        if findall(r"(<a?:\w+:\d+>)+", message.content):
            return

        # Remove codeblocks from message
        msg = message.content
        codeblocks: list = findall(r"(`{1,3}.+?`{1,3})+", msg, flags=DOTALL)

        BLOCK_ID_FORMAT = "<CodeBlock => @Index: {}>"
        for idx, block in enumerate(codeblocks):
            if block.split("`").count("") % 2 != 0:
                continue

            msg = msg.replace(
                block,
                BLOCK_ID_FORMAT.format(idx),
                1
            )

        # Insert space between two ::
        while "::" in msg:
            msg = msg.replace("::", ": :")

        # Search for emojis
        emojis: list = findall(r"(:[\w\-~]*:)+", msg)

        for word in emojis:
            # Continue if already replaced
            if word in temp:
                continue

            try:
                # Get emoji
                emoji = self.emoji_group.get_emoji(word[1:-1])

                # Replace the word by its emoji
                msg = msg.replace(word, str(emoji) if emoji else word)

                # Add the word to temp list to skip it in the next iterations
                if emoji:
                    temp.append(word)

            # Don't do anything if emoji was not found
            except AttributeError as e:
                logging.error(e)

        # Return for no emoji
        if not temp:
            return

        # Add codeblocks back to the message
        for idx, block in enumerate(codeblocks):
            msg = msg.replace(
                BLOCK_ID_FORMAT.format(idx),
                block,
                1
            )

        # Send webhook
        await self._send_webhook(message=message, mod_msg=msg)

        # Delete the original msg
        await message.delete()

    async def _send_webhook(self, message: Message, mod_msg: str = "") -> None:
        """
        Send a webhook

        Args:
            message (Message): Message of a user
        """
        # Get all webhooks currently in the msg channel
        webhooks = await message.channel.webhooks()

        # Check if there exists a webhook with id
        # equal to bot's id. In that case, break
        webhook: Webhook
        for webhook in webhooks:
            if webhook.user.id == self.user.id:
                break

        # Otherwise
        else:
            # Get msg author's avatar
            avatar: bytes = await message.author.display_avatar.read()

            # and create a new webhook for the channel
            webhook: Webhook = await message.channel.create_webhook(
                name="iCODE-BOT",
                avatar=avatar,
                reason="Animated Emoji Usage"
            )

        # Send webhook to the channel with username as the name
        # of msg author and avatar as msg author's avatar
        await webhook.send(content=mod_msg if mod_msg else message.content,
                           username=message.author.display_name,
                           avatar_url=message.author.display_avatar)
