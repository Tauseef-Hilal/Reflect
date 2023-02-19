from collections import OrderedDict
from discord import Emoji, Bot, Guild

from .env import REFLECT_GUILD_ID


class EmojiGroup:
    """
    Handle server emojis
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize and add instance attributes

        Attribute name is Emoji.name
        Attribute value is Emoji.id
        """

        self._bot = bot
        self._emojis = OrderedDict()

        # Iterate through the server emojis
        temp = {}
        emoji: Emoji
        for emoji in self._bot.emojis:
            guild_id = emoji.guild_id

            if not guild_id in self._emojis:
                self._emojis[guild_id] = {}

            i, alias = 2, emoji.name
            while alias in temp:
                alias = alias.split("-")[0] + f"-{i}"
                i += 1

            temp[alias] = guild_id
            if alias != emoji.name and temp[alias.split("-")[0]] != guild_id:
                original = self._emojis[temp[emoji.name]]
                original_alias = f"{emoji.name}-1"

                if not original.get(original_alias):
                    original[original_alias] = original[emoji.name]

                self._emojis[guild_id][emoji.name] = emoji.id

            self._emojis[guild_id][alias] = emoji.id

    def get_emoji(self, name: str, guild_id: int = REFLECT_GUILD_ID) -> Emoji:
        """
        Get emojis

        Args:
            `name` (str): Name of the emoji

        Returns:
            Emoji: emoji for which emoji.name = name
        """

        if guild_id in self._emojis and name in self._emojis[guild_id]:
            return self._bot.get_emoji(self._emojis[guild_id][name])

        # Raise AttributeError if name does not exist
        res = list(filter(
            lambda emojis: name in emojis, self._emojis.values()
        ))

        if not res:
            raise AttributeError(
                f"Object of type EmojiGroup has no attribute {name}"
            )

        # Otherwise return the emoji id
        return self._bot.get_emoji(res[0][name])

    async def update_emojis(self, guild: Guild, updated_emojis=None) -> None:
        """
        Update client emojis
        """

        if updated_emojis:
            self.__init__(self._bot)
            return

        self._emojis[guild.id] = await guild.fetch_emojis()

    def __repr__(self) -> str:
        """
        String representation
        """

        return f"<EmojiGroup => EmojiCount: {len(self._emojis)}>"
