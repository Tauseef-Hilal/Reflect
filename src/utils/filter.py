import logging
from .constants import BADWORDS_FILE


class Filter:
    def __init__(self) -> None:
        """
        Initialize filter
        """
        self._BADWORDS = ""

        # Try to extract words from the file
        try:
            with open(BADWORDS_FILE) as FILE:
                self._BADWORDS = tuple(
                    word.strip() for word in FILE.readlines()
                )

        # Log error if it occurs
        except FileNotFoundError:
            logging.error("Missing data/badwords.txt")

    def has_abusive_words(self, text: str) -> bool:
        """
        Checks a piece of text for abusive words

        Args:
            `text` (str): The text to check

        Returns:
            bool: Whether the text has abusive words or not
        """

        # Split the text into a list of words
        text = text.lower().split()

        # Iterate over the words and check if
        # any is present in _BADWORDS
        for word in text:
            if word in self._BADWORDS:
                return True

        return False
