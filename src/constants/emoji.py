from discord import Emoji, Bot


class EmojiGroup:
    """
    Server emojis
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize
        """

        self.BOT = bot

        emoji: Emoji
        for emoji in self.BOT.emojis:
            setattr(self, emoji.name, emoji.id)

    def get_emoji(self, name: str) -> Emoji:
        """
        Get emojis

        Args:
            name (str): Name of the emoji

        Returns:
            Emoji: emoji for which emoji.name = name
        """

        if not hasattr(self, name):
            raise AttributeError

        return self.BOT.get_emoji(getattr(self, name))

    def update_emojis(self) -> None:
        """
        Update emoji attrs
        """

        emoji: Emoji
        for emoji in self.BOT.emojis:
            if hasattr(self, emoji.name):
                continue

            setattr(self, emoji.name, emoji.id)

    def __repr__(self) -> str:
        """
        String representation
        """

        return f"<EmojiGroup => EmojiCount: {len(vars(self)) - 1}>"
