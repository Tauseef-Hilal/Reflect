import functools
from discord import (
    ApplicationContext,
    TextChannel,
    Permissions,
    Embed
)

from .color import Colors


def under_maintenance(ctx: ApplicationContext) -> bool:
    """
    Check if the bot is under maintenance

    Args:
        `channel` (TextChannel): The channel from which a cmd was run

    Returns:
        bool: True if under maintenance
    """

    # If the bot is running under maintenance mode
    # and the channel is not the maintenance channel
    if (ctx.bot.MAINTENANCE_MODE
            and ctx.channel != ctx.bot.MAINTENANCE_CHANNEL):

        # Dispatch maintenance event
        ctx.bot.dispatch("maintenance", ctx)
        return True
    
    return False


async def has_permissions(ctx: ApplicationContext, **perms) -> bool:
    """
    Check whether a member has required permissions to
    run a command

    Returns:
        bool: True if the member has all of the perms
    """

    # Get channel and permissions of the author in that channel
    channel: TextChannel = ctx.channel
    permissions: Permissions = channel.permissions_for(ctx.author)

    # Find missing permissions
    try:
        missing = []
        for perm, value in perms.items():
            if getattr(permissions, perm) != value:
                missing.append(perm)
    except AttributeError:
        if not await ctx.bot.is_owner(ctx.author):
            missing.append(perm)

    # Return true if the author has all the required permissions
    if not missing:
        return True

    # Otherwise show error message to the member
    emoji = ctx.bot.emoji_group.get_emoji("red_cross", ctx.guild_id)
    await ctx.respond(
        embed=Embed(
            title=f"Permission Error {emoji}",
            description="You do not have the required permissions"
                        " to run this command.",
            color=Colors.RED
        ),
        delete_after=3
    )

    return False


def permission_check(**perms):
    """
    Check whether a member has required permissions to
    run a command
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if await has_permissions(args[1], **perms):
                await func(*args, **kwargs)

        return wrapper
    return decorator


def maintenance_check():
    """
    Check if the bot is running under maintenance
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not under_maintenance(args[1]):
                await func(*args, **kwargs)

        return wrapper
    return decorator
