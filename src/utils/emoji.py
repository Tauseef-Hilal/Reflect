import logging
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
        i = 0
        for emoji in self.BOT.emojis:
            name = emoji.name
            # Check if the emoji.name is already taken
            while hasattr(self, name):
                i += 1
                name += f"-{i}"

            # Set attr for each emoji
            setattr(self, name, emoji.id)

    def get_emoji(self, name: str) -> Emoji:
        """
        Get emojis

        Args:
            `name` (str): Name of the emoji

        Returns:
            Emoji: emoji for which emoji.name = name
        """

        # Raise AttributeError if param: name does not
        # match any of the instance attributes
        if not hasattr(self, name):
            raise AttributeError(
                f"Object of type EmojiGroup has no attribute {name}"
            )

        # Others return the Emoji with the given name
        return self.BOT.get_emoji(getattr(self, name))

    def update_emojis(self) -> None:
        """
        Update instance attributes
        """
        
        # Delete all emojis
        bot = self.BOT
        vars(self).clear()
        
        # Update emojis
        self.__init__(bot)

        # emoji: Emoji
        # # Add new emojis
        # for emoji in self.BOT.emojis:
        #     # Skip existing attributes
        #     if hasattr(self, emoji.name):
        #         continue

        #     # Create new attributes
        #     setattr(self, emoji.name, emoji.id)
        #     logging.info(f"Added new emoji: {emoji.name}")
        
        # # Remove deleted emojis
        # for emoji_name in vars(self):
        #     if emoji_name not in self.BOT.emojis:
        #         delattr(self, emoji_name)
        #         logging.info(f"Deleted emoji: {emoji_name}")

    def __repr__(self) -> str:
        """
        String representation
        """

        return f"<EmojiGroup => EmojiCount: {len(vars(self)) - 1}>"
