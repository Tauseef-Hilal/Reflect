import asyncio
import logging
from random import choice
from datetime import datetime
from re import (
    DOTALL,
    findall
)

from discord import (
    Bot,
    Game,
    Guild,
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
    ICODIAN_ROLE_ID,
    STAFF_CHANNEL_ID,
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

        self.ICODE_GUILD = self.get_guild(ICODE_GUILD_ID)
        if not self.ICODE_GUILD:
            logging.warning("Couldn't find iCODE")

        # Start bump timer
        for guild_data in self.db.find():
            logging.info(
                f"Getting previous bump time for {guild_data['guild_id']}"
            )

            try:
                previous_bump_time = self.bump_timer.get_bump_time(guild_data)
            except (TypeError, KeyError):
                logging.warning("No bump data found")
                continue

            logging.info(f"Previous bump time: {previous_bump_time}")

            delta = (datetime.now() - previous_bump_time).total_seconds()
            delay = 0 if delta >= 7200 else (7200 - delta)

            self.dispatch("bump_done", guild_data, int(delay))

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

        try:
            guild: Guild = self.get_guild(payload.guild_id)
            guild_data = self.db.find_one({"guild_id": guild.id})
            rxn_messages = guild_data["reaction_messages"]

        except (KeyError, TypeError):
            return

        for rxn_msg in rxn_messages:
            if int(rxn_msg) == payload.message_id:
                break
        else:
            return

        emoji: PartialEmoji = payload.emoji

        try:
            role: Role = guild.get_role(rxn_messages[rxn_msg][emoji.name])
        except KeyError:
            pass
        else:
            if role:
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
        try:
            guild: Guild = self.get_guild(payload.guild_id)
            guild_data = self.db.find_one({"guild_id": guild.id})
            rxn_messages = guild_data["reaction_messages"]

        except (KeyError, TypeError):
            return

        for rxn_msg in rxn_messages:
            if int(rxn_msg) == payload.message_id:
                break
        else:
            return

        emoji: PartialEmoji = payload.emoji

        try:
            role: Role = guild.get_role(rxn_messages[rxn_msg][emoji.name])
        except KeyError:
            pass
        else:
            member: Member = await guild.fetch_member(payload.user_id)

            if member and role:
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
            guild_data = self.db.find_one({"guild_id": member.guild.id})
            channel = self.get_channel(
                guild_data["channel_ids"]["console_channel"]
            )
            assert isinstance(channel, TextChannel)
        except (KeyError, TypeError, AssertionError):
            return

        # Send embed with random welcome msg to console channel
        await channel.send(
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
            guild_data = self.db.find_one({"guild_id": member.guild.id})
            channel = self.get_channel(
                guild_data["channel_ids"]["console_channel"]
            )
            assert isinstance(channel, TextChannel)
        except (KeyError, TypeError, AssertionError):
            return

        # Send embed with random farewell msg to receiver channel
        await channel.send(
            embed=Embed(
                description=choice(
                    FAREWELL_MESSAGES
                ).format(
                    member.display_name
                ),
                color=Colors.RED
            )
        )

    async def on_bump_done(self, guild_data: dict, delay: int) -> None:
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
            channel = self.get_channel(
                guild_data["channel_ids"]["bump_reminder_channel"]
            )
            assert isinstance(channel, TextChannel)

            # Get bumper role
            bumper = channel.guild.get_role(
                guild_data["role_ids"]["server_bumper_role"]
            )
            assert isinstance(bumper, Role)
        except (KeyError, TypeError, AssertionError):
            logging.warning("Reminder channel or bumper role not set")

            if not channel:
                emoji = self.emoji_group.get_emoji("warning")
                for channel in self.get_guild(guild_data["guild_id"]).text_channels:
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
            guild_data = self.db.find_one({"guild_id": message.guild.id})
            channel = self.get_channel(
                guild_data["channel_ids"]["modlogs_channel"]
            )
            assert isinstance(channel, TextChannel)
        except (KeyError, TypeError, AssertionError):
            return

        attachments = "\n".join(
            [f"[{attachment.filename}]({attachment.url})"
             for attachment in message.attachments]
        )
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
                value=attachments if attachments else "[No Attachments]"
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

                try:
                    self.bump_timer.update_bump_time(
                        self.db, message.guild.id, datetime.now()
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
                    guild_data = self.db.find_one(
                        {"guild_id": message.guild.id}
                    )
                    self.dispatch("bump_done", guild_data, 7200)
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
        processedCount = 0

        # Return if under maintenance
        if (self.MAINTENANCE_MODE and
                message.channel != self.MAINTENANCE_CHANNEL):
            return

        # Insert space between two :: and ><
        msg = message.content
        while "::" in msg:
            msg = msg.replace("::", ": :")

        while "><" in msg:
            msg = msg.replace("><", "> <")

        # Search for emojis
        emojis: set = set(findall(r"(:[\w\-~]*:)+", msg))
        processed_emojis: dict = {
            f":{emoji.split(':')[1]}:":True 
            for emoji in findall(r"(<a?:\w+:\d+>)+", msg)
        }

        # Return if all emojis are already processed
        if len(emojis) - len(processed_emojis) == 0:
            return

        # Remove codeblocks from message
        codeblocks: set = set(
            findall(r"(`{1,3}.+?`{1,3})+", msg, flags=DOTALL)
        )

        BLOCK_ID_FORMAT = "<CodeBlock => @Index: {}>"
        for idx, block in enumerate(codeblocks):
            if block.split("`").count("") % 2 != 0:
                continue

            msg = msg.replace(block, BLOCK_ID_FORMAT.format(idx))

        for word in emojis:
            # Skip if already processed
            if word in processed_emojis:
                continue

            try:
                # Get emoji
                emoji = self.emoji_group.get_emoji(word[1:-1])

                # Skip if not a valid emoji
                if not emoji:
                    continue

                # Replace the word by its emoji
                msg = msg.replace(word, str(emoji))
                processedCount += 1

            # Don't do anything if emoji was not found
            except AttributeError as e:
                logging.error(e)

        # Return for no emoji
        if processedCount == 0:
            return

        # Add codeblocks back to the message
        for idx, block in enumerate(codeblocks):
            msg = msg.replace(BLOCK_ID_FORMAT.format(idx), block)

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
