from discord import Emoji, Bot


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
        self._emojis = {}

        # Iterate through the server emojis
        emoji: Emoji
        for emoji in self._bot.emojis:
            guild_id = emoji.guild_id
            
            if not guild_id in self._emojis:
                self._emojis[guild_id] = {}
            
            self._emojis[guild_id][emoji.name] = emoji.id

    def get_emoji(self, name: str, guild_id: int) -> Emoji:
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
        res = list(filter(lambda d: name in d, self._emojis.values()))
        if not res:
            raise AttributeError(
                f"Object of type EmojiGroup has no attribute {name}"
            )

        # Otherwise return the emoji id
        return self._bot.get_emoji(res[0][name])

    def update_emojis(self) -> None:
        """
        Update instance attributes
        """
        
        # Delete all emojis
        bot = self._bot
        vars(self).clear()
        
        # Update emojis
        self.__init__(bot)

    def __repr__(self) -> str:
        """
        String representation
        """

        return f"<EmojiGroup => EmojiCount: {len(vars(self)) - 1}>"
