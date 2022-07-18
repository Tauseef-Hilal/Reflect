from discord import (
    ApplicationCommandInvokeError,
    Interaction,
    Message,
    Cog,
    Embed,
    NotFound,
    Option,
    Reaction,
    Role,
    SlashCommandGroup,
    ApplicationContext
)

from typing import List, Tuple

from ..bot import ICodeBot
from ..utils.color import Colors
from ..utils.checks import (
    maintenance_check,
    permission_check,
)


class ReactionRoleCommands(Cog):
    """
    Commands for reaction roles
    """

    RR = SlashCommandGroup(
        "reaction-roles",
        "Reaction role commands",
        [963337124176879696]
    )

    def __init__(self, bot: ICodeBot) -> None:
        """
        Initialize

        Args:
            bot (discord.Bot): iCODE-BOT
        """
        super().__init__()
        self._bot = bot

    @RR.command(name="add")
    @maintenance_check()
    @permission_check(manage_roles=True)
    async def _add(
        self,
        ctx: ApplicationContext,
        message_id: Option(str, "Message ID"),
        roles: Option(
            str,
            "String of role names separated by `-`. "
            "Must have the order of reactions"
        )
    ) -> None:
        """
        Set a message for reaction roles

        Args:
            ctx (ApplicationContext)
            message (Option): Message
        """

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting up reaction roles for the message "
                            f"{emoji}",
                color=Colors.GOLD
            )
        )

        message: Message = self._bot.get_message(int(message_id))
        if not message:
            try:
                message: Message = await ctx.channel.fetch_message(
                    int(message_id)
                )
            except NotFound:
                emoji = self._bot.emoji_group.get_emoji("red_cross")

                await res.edit_original_message(
                    embed=Embed(
                        title=f"Error fetching message {emoji}",
                        description="Please try again from the same "
                                    "channel where the message exists",
                        color=Colors.RED
                    ),
                    delete_after=3
                )

                return

        msg_reactions: List[Reaction] = message.reactions

        roles = roles.split("-")
        if len(roles) != len(msg_reactions):
            emoji = self._bot.emoji_group.get_emoji("red_cross")

            if not len(msg_reactions):
                msg = ("Target message must have added reactions and\n "
                       "`reactionCount` must be equal to `roleCount`")
            else:
                msg = ("`roles` must be a string of roles separated "
                       "by `-` corresponding to the reaction order.")

            await res.edit_original_message(
                embed=Embed(
                    title=f"Error setting reaction roles {emoji}",
                    description=msg,
                    color=Colors.RED
                ),
                delete_after=3
            )
            return

        reaction_roles: List[Role] = []
        guild_roles: List[Role] = await ctx.guild.fetch_roles()
        for role in roles:
            for guild_role in guild_roles:
                if guild_role.name == role:
                    reaction_roles.append(guild_role)
                    break
            else:
                await res.edit_original_message(
                    embed=Embed(
                        description=f"{emoji} Role `{role}` does not exist",
                        color=Colors.RED
                    ),
                    delete_after=5
                )

                return

        rxn_data = {}
        for reaction, role in zip(msg_reactions, reaction_roles):
            if isinstance(reaction.emoji, str):
                rxn_data[reaction.emoji] = role.id
                continue

            rxn_data[reaction.emoji.name] = role.id

        try:
            rxn_messages = self._bot.db.find_one(
                {"guild_id": ctx.guild.id}
            )["reaction_messages"]

            rxn_messages[message_id] = rxn_data
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": rxn_messages
                    }
                }
            )
        except KeyError:
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": {
                            message_id: rxn_data
                        }
                    }
                }
            )
        except TypeError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await res.edit_original_message(
                embed=Embed(
                    description=f"{emoji} Reaction roles not set. Use "
                                "`/setup` command to set up reaction roles.",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Reaction roles set "
                            f"{emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )

    @RR.command(name="remove")
    @maintenance_check()
    @permission_check(manage_roles=True)
    async def _remove(
        self,
        ctx: ApplicationContext,
        message_id: Option(str, "Message ID")
    ) -> None:
        """
        Set a message for reaction roles

        Args:
            ctx (ApplicationContext)
            message (Option): Message
        """

        # ---
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Removing reaction roles from the message "
                            f"{emoji}",
                color=Colors.GOLD
            )
        )

        try:
            rxn_messages = self._bot.db.find_one(
                {"guild_id": ctx.guild.id}
            )["reaction_messages"]

            rxn_messages.pop(message_id)
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": rxn_messages
                    }
                }
            )
        except KeyError:
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": {}
                    }
                }
            )
        except TypeError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await res.edit_original_message(
                embed=Embed(
                    description=f"{emoji} Reaction roles not set. Use "
                                "`/setup` command to set up reaction roles.",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        # ---
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_message(
            embed=Embed(
                description=f"Reaction roles removed "
                            f"{emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
