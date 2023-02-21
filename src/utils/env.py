import os
import logging

from dotenv import load_dotenv

# Load .env
load_dotenv(".env")

# ENV CONSTANTS
REFLECT_GUILD_ID = int(os.getenv("REFLECT_GUILD_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    assert REFLECT_GUILD_ID is not None
    assert BOT_TOKEN is not None
except AssertionError:
    logging.log(level=logging.ERROR, msg="Missing .env file")
