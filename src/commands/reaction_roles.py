from discord import (
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

from typing import List

from ..bot import Reflect
from ..utils.color import Colors
from ..utils.checks import (
    maintenance_check,
    permission_check,
)


class ReactionRoleCommands(Cog):
    """
    Commands for reaction roles
    """

    # Create command group
    RR = SlashCommandGroup(
        "reaction-roles",
        "Reaction role commands"
    )

    def __init__(self, bot: Reflect) -> None:
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Setting up reaction roles for the message "
                            f"{emoji}",
                color=Colors.GOLD
            )
        )

        # Try to find the message
        message: Message = self._bot.get_message(int(message_id))

        # If not successful
        if not message:
            # Try to fetch the message
            try:
                message: Message = await ctx.channel.fetch_message(
                    int(message_id)
                )

            # If still not able to find
            except NotFound:
                emoji = self._bot.emoji_group.get_emoji("red_cross")

                # Send Error msg to the channel
                await res.edit_original_response(
                    embed=Embed(
                        title=f"Error fetching message {emoji}",
                        description="Please try again from the same "
                                    "channel where the message exists",
                        color=Colors.RED
                    ),
                    delete_after=3
                )

                return

        # Determine msg reactions
        msg_reactions: List[Reaction] = message.reactions

        # Create a list out of the roles argument
        roles = roles.split("-")

        # Send error msg if the number of roles is not equal to the number
        # of reactions on the message
        if len(roles) != len(msg_reactions):
            emoji = self._bot.emoji_group.get_emoji("red_cross")

            # Determine the error msg to send
            if not len(msg_reactions):
                msg = ("Target message must have added reactions and\n "
                       "`reactionCount` must be equal to `roleCount`")
            else:
                msg = ("`roles` must be a string of roles separated "
                       "by `-` corresponding to the reaction order.")

                # Send error msg
                await res.edit_original_response(
                    embed=Embed(
                        title=f"Error setting reaction roles {emoji}",
                        description=msg,
                        color=Colors.RED
                    ),
                    delete_after=3
                )
            return

        # Create an empty list of reaction roles
        reaction_roles: List[Role] = []

        # Get guild roles
        guild_roles: List[Role] = await ctx.guild.fetch_roles()

        # Validate the roles arg
        for role in roles:
            for guild_role in guild_roles:
                if guild_role.name == role:
                    reaction_roles.append(guild_role)
                    break

            # Send error msg in case of invalid role
            else:
                await res.edit_original_response(
                    embed=Embed(
                        description=f"{emoji} Role `{role}` does not exist",
                        color=Colors.RED
                    ),
                    delete_after=5
                )

                return

        # Add reactions to the msg
        for rxn in msg_reactions:
            await message.add_reaction(rxn)

        # Prepare data to send to the db
        rxn_data = {}
        for reaction, role in zip(msg_reactions, reaction_roles):
            if isinstance(reaction.emoji, str):
                rxn_data[reaction.emoji] = role.id
                continue

            rxn_data[reaction.emoji.name] = role.id

        # Try to get the already existing reaction data
        try:
            rxn_messages = self._bot.db.find_one(
                {"guild_id": ctx.guild.id}
            )["reaction_messages"]

            # Update data
            rxn_messages[message_id] = rxn_data
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": rxn_messages
                    }
                }
            )

        # If not successful
        except KeyError:

            # Create new reaction data
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

        # Send msg to setup reaction roles
        except TypeError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await res.edit_original_response(
                embed=Embed(
                    description=f"{emoji} Reaction roles not set. Use "
                                "`/setup` command to set up reaction roles.",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        # Prmopt success msg
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_response(
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

        # Send animation embed
        emoji = self._bot.emoji_group.get_emoji("loading_dots")
        res: Interaction = await ctx.respond(
            embed=Embed(
                description=f"Removing reaction roles from the message "
                            f"{emoji}",
                color=Colors.GOLD
            )
        )

        # Try to get the reaction data
        try:
            rxn_messages = self._bot.db.find_one(
                {"guild_id": ctx.guild.id}
            )["reaction_messages"]

            # Remove the key equal to message id
            rxn_messages.pop(message_id)
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": rxn_messages
                    }
                }
            )

        # Create new reaction data if not already there
        except KeyError:
            self._bot.db.update_one(
                self._bot.db.find_one(filter={"guild_id": ctx.guild.id}),
                {
                    "$set": {
                        "reaction_messages": {}
                    }
                }
            )

        # Send msg to setup reaction roles
        except TypeError:
            emoji = self._bot.emoji_group.get_emoji("warning")
            await res.edit_original_response(
                embed=Embed(
                    description=f"{emoji} Reaction roles not set. Use "
                                "`/setup` command to set up reaction roles.",
                    color=Colors.RED
                ),
                delete_after=5
            )
            return

        # Prompt success
        emoji = self._bot.emoji_group.get_emoji("green_tick")
        await res.edit_original_response(
            embed=Embed(
                description=f"Reaction roles removed "
                            f"{emoji}",
                color=Colors.GREEN
            ),
            delete_after=2
        )
