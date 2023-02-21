from pymongo import MongoClient
from pymongo.collection import Collection


def get_database(host: str) -> Collection:
    """
    Get guild database

    Args:
        host (str): MONGO_DB URI

    Returns:
        Collection: A collection of documents
    """
    CLIENT = MongoClient(host=host)

    # Create the database
    return CLIENT["reflect"]["guilds"]
