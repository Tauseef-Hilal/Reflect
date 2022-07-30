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

    # Create command group
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for "
                            f"moderation logs {emoji}",
                color=Colors.GOLD
            )
        )

        # Check if guild document is created
        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):

            # Create new document
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "modlogs_channel": channel.id
                    }
                }
            )

        # If it is
        else:
            # Try to get channel ids
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                # Update channel ids
                channel_ids["modlogs_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )

            # Create new channel ids key if it doesnot exist
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

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick", ctx.guild.id)
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

        # Send animation msg
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for bump "
                            f"reminders {emoji}",
                color=Colors.GOLD
            )
        )

        # Check if guild document is created
        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):

            # Create new document
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "bump_reminder_channel": channel.id
                    }
                }
            )

        # If it is
        else:

            # Try to get channel ids
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                # Update channel ids
                channel_ids["bump_reminder_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )

            # Create new channel ids if it doesnt exist
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

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick", ctx.guild.id)
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {role.mention} for bump "
                            f"reminder pings {emoji}",
                color=Colors.GOLD
            )
        )

        # Check if guild document is created
        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):

            # Create new document
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "role_ids": {
                        "server_bumper_role": role.id
                    }
                }
            )

        # If it is
        else:
            # Try to get role ids
            try:
                role_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["role_ids"]

                # Update role ids
                role_ids["server_bumper_role"] = role.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "role_ids": role_ids
                        }
                    }
                )

            # Create new role ids key if it doesnot exist
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

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick", ctx.guild.id)
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for member "
                            f"join/leave events {emoji}",
                color=Colors.GOLD
            )
        )

        # Check if guild document is created
        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):

            # Create new document
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "console_channel": channel.id
                    }
                }
            )

        # If it is
        else:
            # Try to get channel ids
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                # Update channel ids
                channel_ids["console_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )

            # Create new channel ids key if it doesnot exist
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
        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick", ctx.guild.id)
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting {channel.mention} for suggestions "
                            f"{emoji}",
                color=Colors.GOLD
            )
        )

        # Check if guild document is created
        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):

            # Create new document
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "channel_ids": {
                        "suggestions_channel": channel.id
                    }
                }
            )

        # If it is
        else:
            # Try to get channel ids
            try:
                channel_ids = self._bot.db.find_one(
                    {"guild_id": guild.id}
                )["channel_ids"]

                # Update channel ids
                channel_ids["suggestions_channel"] = channel.id
                self._bot.db.update_one(
                    self._bot.db.find_one(filter={"guild_id": guild.id}),
                    {
                        "$set": {
                            "channel_ids": channel_ids
                        }
                    }
                )

            # Create new channel ids key if it doesnot exist
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

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick", ctx.guild.id)
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots", ctx.guild.id)
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting up reaction roles {emoji}",
                color=Colors.GOLD
            )
        )

        # Check if guild document is created
        guild: Guild = ctx.guild
        if not self._bot.db.find_one(filter={"guild_id": guild.id}):

            # Create new document
            self._bot.db.insert_one(
                {
                    "guild_id": guild.id,
                    "reaction_messages": {}
                }
            )

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick", ctx.guild.id)
        await res.edit_original_message(
            embed=Embed(
                description=f"Set up reaction roles {emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
