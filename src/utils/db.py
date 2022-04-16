import datetime

from pymongo import MongoClient
from pymongo.database import Database


def get_database(host: str) -> Database:
    """
    Get guild database

    Args:
        host (str): MONGO_DB URI

    Returns:
        Database: Database
    """
    CLIENT = MongoClient(host=host)

    # Create the database
    return CLIENT["guilds"]



