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

        self.BOT = bot

        # Iterate through the server emojis
        emoji: Emoji
        for emoji in self.BOT.emojis:
            # Set attr for each emoji
            setattr(self, emoji.name, emoji.id)

    def get_emoji(self, name: str) -> Emoji:
        """
        Get emojis

        Args:
            name (str): Name of the emoji

        Returns:
            Emoji: emoji for which emoji.name = name
        """

        # Raise AttributeError if param: name does not
        # match any of the instance attributes
        if not hasattr(self, name):
            raise AttributeError

        # Others return the Emoji with the given name
        return self.BOT.get_emoji(getattr(self, name))

    def update_emojis(self) -> None:
        """
        Update instance attributes
        """

        emoji: Emoji
        for emoji in self.BOT.emojis:
            # Skip existing attributes
            if hasattr(self, emoji.name):
                continue

            # Create new attributes
            setattr(self, emoji.name, emoji.id)

    def __repr__(self) -> str:
        """
        String representation
        """

        return f"<EmojiGroup => EmojiCount: {len(vars(self)) - 1}>"
