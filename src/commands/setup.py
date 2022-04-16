from discord import (
    Cog,
    Embed,
    Guild,
    Interaction,
    Option,
    Role,
    SlashCommandGroup,
    ApplicationContext,
    TextChannel
)

from ..utils.color import Colors
from ..bot import ICodeBot
from .general import (
    under_maintenance,
    has_permissions
)


class SetupCommands(Cog):
    """
    Commands for setup
    """

    SETUP = SlashCommandGroup(
        "setup",
        "Commands for setting bot features."
    )

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize
        """

        super().__init__()
        self._bot = bot

    @SETUP.command(name="modlogs")
    async def _modlogs(
            self,
            ctx: ApplicationContext,
            channel: Option(
                TextChannel,
                "The channel where you want to log. "
                "Defaults to the current channel"
            ) = None
    ) -> None:
        """
        Setup a channel for moderation logs

        Args:
            ctx (ApplicationContext)
            channel (TextChannel): The log channel
        """

        # Check for maintenance and permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"administrator": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # Select current channel if no channel provided
        if not channel:
            channel: TextChannel = ctx.channel

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for "
                            f"moderation logs {emoji}",
                color=Colors.GOLD
            )
        )

        guild: Guild = ctx.guild
        if str(guild.id) not in self._bot.db.list_collection_names():
            collection = self._bot.db.create_collection(str(guild.id))
            collection.insert_one(
                {
                    "channel_ids": {
                        "modlogs_channel": channel.id
                    }
                }
            )
            return

        collection = self._bot.db.get_collection(str(guild.id))
        if "channel_ids" in collection.find_one():
            channels_dict = collection.find_one()["channel_ids"]
            channels_dict["modlogs_channel"] = channel.id

            collection.update_one(
                collection.find_one(),
                {"$set": {"channel_ids": channels_dict}}
            )
        else:
            collection.update_one(
                collection.find_one(),
                {"$set":
                    {
                        "channel_ids": {
                            "modlogs_channel": channel.id
                        }
                    }
                 }
            )

        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {channel.mention} for "
                            f"moderation logs {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @SETUP.command(name="bump-reminder")
    async def _bump_timer(
            self,
            ctx: ApplicationContext,
            channel: Option(
                TextChannel,
                "The channel where you want to send reminder. "
                "Defaults to the current channel"
            ) = None
    ) -> None:
        """
        Setup a channel for bump reminder

        Args:
            ctx (ApplicationContext)
            channel (TextChannel): The reminder channel
        """

        # Check for maintenance and permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"administrator": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # Select current channel if no channel provided
        if not channel:
            channel: TextChannel = ctx.channel

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for bump "
                            f"reminders {emoji}",
                color=Colors.GOLD
            )
        )

        guild: Guild = ctx.guild
        if str(guild.id) not in self._bot.db.list_collection_names():
            collection = self._bot.db.create_collection(str(guild.id))
            collection.insert_one(
                {
                    "channel_ids": {
                        "bump_reminder_channel": channel.id
                    }
                }
            )
            return

        collection = self._bot.db.get_collection(str(guild.id))
        if "channel_ids" in collection.find_one():
            channels_dict = collection.find_one()["channel_ids"]
            channels_dict["bump_reminder_channel"] = channel.id

            collection.update_one(
                collection.find_one(),
                {"$set": {"channel_ids": channels_dict}}
            )
        else:
            collection.update_one(
                collection.find_one(),
                {"$set":
                    {
                        "channel_ids": {
                            "bump_reminder_channel": channel.id
                        }
                    }
                 }
            )

        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {channel.mention} for bump "
                            f"reminders {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @SETUP.command(name="bumper-role")
    async def _bumper_role(
            self,
            ctx: ApplicationContext,
            role: Option(
                Role,
                "The role to ping in bump reminder message."
            )
    ) -> None:
        """
        Setup a role for bump reminder pings

        Args:
            ctx (ApplicationContext)
            role (Role): The bumper role
        """

        # Check for maintenance and permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"administrator": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {role.mention} for bump "
                            f"reminder pings {emoji}",
                color=Colors.GOLD
            )
        )

        guild: Guild = ctx.guild
        if str(guild.id) not in self._bot.db.list_collection_names():
            collection = self._bot.db.create_collection(str(guild.id))
            collection.insert_one(
                {
                    "role_ids": {
                        "server_bumper_role": role.id
                    }
                }
            )
            return

        collection = self._bot.db.get_collection(str(guild.id))
        if "role_ids" in collection.find_one():
            roles_dict = collection.find_one()["role_ids"]
            roles_dict["server_bumper_role"] = role.id

            collection.update_one(
                collection.find_one(),
                {"$set": {"role_ids": roles_dict}}
            )
        else:
            collection.update_one(
                collection.find_one(),
                {"$set":
                    {
                        "role_ids": {
                            "server_bumper_role": role.id
                        }
                    }
                 }
            )

        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {role.mention} for bump "
                            f"reminder pings {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @SETUP.command(name="console")
    async def _console(
            self,
            ctx: ApplicationContext,
            channel: Option(
                TextChannel,
                "The channel where you want to welcome new users. "
                "Defaults to the current channel"
            ) = None
    ) -> None:
        """
        Setup a channel for member join/leave events

        Args:
            ctx (ApplicationContext)
            channel (TextChannel): The welcome channel
        """

        # Check for maintenance and permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"administrator": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # Select current channel if no channel provided
        if not channel:
            channel: TextChannel = ctx.channel

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for member "
                            f"join/leave events {emoji}",
                color=Colors.GOLD
            )
        )

        guild: Guild = ctx.guild
        if str(guild.id) not in self._bot.db.list_collection_names():
            collection = self._bot.db.create_collection(str(guild.id))
            collection.insert_one(
                {
                    "channel_ids": {
                        "console_channel": channel.id
                    }
                }
            )
            return

        collection = self._bot.db.get_collection(str(guild.id))
        if "channel_ids" in collection.find_one():
            channels_dict = collection.find_one()["channel_ids"]
            channels_dict["console_channel"] = channel.id

            collection.update_one(
                collection.find_one(),
                {"$set": {"channel_ids": channels_dict}}
            )
        else:
            collection.update_one(
                collection.find_one(),
                {"$set":
                    {
                        "channel_ids": {
                            "console_channel": channel.id
                        }
                    }
                 }
            )
        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {channel.mention} for member "
                            f"join/leave events{emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @SETUP.command(name="suggestions")
    async def _suggestions(
            self,
            ctx: ApplicationContext,
            channel: Option(
                TextChannel,
                "The channel where you want to put suggestions. "
                "Defaults to the current channel"
            ) = None
    ) -> None:
        """
        Setup a channel for suggestions

        Args:
            ctx (ApplicationContext)
            channel (TextChannel): The welcome channel
        """

        # Check for maintenance and permissions
        if (
            not await has_permissions(
                self._bot,
                ctx,
                **{"administrator": True}
            )
            or under_maintenance(self._bot, ctx)
        ):
            return

        # Select current channel if no channel provided
        if not channel:
            channel: TextChannel = ctx.channel

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for suggestions "
                            f"{emoji}",
                color=Colors.GOLD
            )
        )

        guild: Guild = ctx.guild
        if str(guild.id) not in self._bot.db.list_collection_names():
            collection = self._bot.db.create_collection(str(guild.id))
            collection.insert_one(
                {
                    "channel_ids": {
                        "suggestions_channel": channel.id
                    }
                }
            )
            return

        collection = self._bot.db.get_collection(str(guild.id))
        if "channel_ids" in collection.find_one():
            channels_dict = collection.find_one()["channel_ids"]
            channels_dict["suggestions_channel"] = channel.id

            collection.update_one(
                collection.find_one(),
                {"$set": {"channel_ids": channels_dict}}
            )
        else:
            collection.update_one(
                collection.find_one(),
                {"$set":
                    {
                        "channel_ids": {
                            "suggestions_channel": channel.id
                        }
                    }
                 }
            )
        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {channel.mention} for member "
                            f"join/leave events{emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
