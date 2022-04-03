import logging
from .constants import BADWORDS_FILE


class Filter:
    def __init__(self) -> None:
        """
        Initialize filter
        """
        self._BADWORDS = ""

        try:
            with open(BADWORDS_FILE) as FILE:
                self._BADWORDS = tuple(
                    word.strip() for word in FILE.readlines()
                )

        except FileNotFoundError:
            logging.error("Missing data/badwords.txt")

    def has_abusive_words(self, text: str) -> bool:
        """
        Checks a piece of text for abusive words

        Args:
            text (str): The text to check

        Returns:
            bool: Whether the text has abusive words or not
        """

        text = text.lower().split()
        for word in text:
            if word in self._BADWORDS:
                return True

        return False
