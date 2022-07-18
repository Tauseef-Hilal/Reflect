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
from ..utils.checks import (
    maintenance_check,
    permission_check
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
    @maintenance_check()
    @permission_check(administrator=True)
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
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "modlogs_channel": channel.id
                    }
                }
            )
        else:
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                channel_ids["modlogs_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )
            except KeyError:
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
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
    @maintenance_check()
    @permission_check(administrator=True)
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
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "bump_reminder_channel": channel.id
                    }
                }
            )
        else:
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                channel_ids["bump_reminder_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )
            except KeyError:
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
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
    @maintenance_check()
    @permission_check(administrator=True)
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
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "role_ids": {
                        "server_bumper_role": role.id
                    }
                }
            )
        else:
            try:
                role_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["role_ids"]

                role_ids["server_bumper_role"] = role.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "role_ids": role_ids
                        }
                    }
                )
            except KeyError:
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
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
    @maintenance_check()
    @permission_check(administrator=True)
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
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "console_channel": channel.id
                    }
                }
            )
        else:
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                channel_ids["console_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )
            except KeyError:
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": {
                                "console_channel": channel.id
                            }
                        }
                    }
                )
        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {channel.mention} for member "
                            f"join/leave events {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @SETUP.command(name="suggestions")
    @maintenance_check()
    @permission_check(administrator=True)
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
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "suggestions_channel": channel.id
                    }
                }
            )
        else:
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                channel_ids["suggestions_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )
            except KeyError:
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": {
                                "suggestions_channel": channel.id
                            }
                        }
                    }
                )

        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set {channel.mention} for suggestions "
                            f"{emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @SETUP.command(name="reaction-roles")
    @maintenance_check()
    @permission_check(administrator=True)
    async def _reaction_roles(
            self,
            ctx: ApplicationContext
    ) -> None:
        """
        Setup reaction roles

        Args:
            ctx (ApplicationContext)
        """

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting up reaction roles {emoji}",
                color=Colors.GOLD
            )
        )

        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "reaction_messages": {}
                }
            )

        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Set up reaction roles {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
