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
                self._BADWORDS = set(
                    word.strip() for word in FILE.readlines()
                )

        # Log error if it occurs
        except FileNotFoundError:
            logging.error("Missing data/badwords.txt")

    def has_abusive_words(self, text: str) -> str:
        """
        Checks a piece of text for abusive words

        Args:
            `text` (str): The text to check

        Returns:
            str: The bad word which was used
        """

        # Setup
        text = text.replace("`", "").replace("*", "")

        # Split the text into a list of words
        text = text.lower().split()

        # Iterate over the words and check if
        # any is present in _BADWORDS
        for word in text:
            if self._BADWORDS.get(word):
                return word

        return ""

    def censor(self, text: str) -> str:
        """
        Censor a piece of text

        Args:
            `text` (str): The text to censor

        Returns:
            str: The censored text.
        """

        # Setup
        text = text.replace("`", "").replace("*", "")

        # Split the text into a list of words
        words = text.split()

        # Iterate over the words and check if
        # any is present in _BADWORDS
        for word in words:
            if word.lower() not in self._BADWORDS:
                continue

            if len(word) < 6:
                stars = "\*" * (len(word) - 2)
                text = text.replace(
                    word,
                    f"|| {word[0]}{stars}{word[-1]} ||",
                    1
                )
            else:
                stars = "\*" * (len(word) - 4)
                text = text.replace(
                    word,
                    f"|| {word[:2]}{stars}{word[-2:]} ||",
                    1
                )

        return text
