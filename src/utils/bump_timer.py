import datetime
import pymongo


class BumpTimer(pymongo.MongoClient):
    """
    Feature: Bump Reminder
    """

    def __init__(self, host, **kwargs) -> None:
        """
        Initialize

        Args:
            host (str): MONGO_DB URI
        """
        super().__init__(host, **kwargs)
        self.DB = self["bump_time"]
        self.COLLECTION = self.DB["bump"]

    def update_bump_time(self, timestamp: datetime.datetime) -> None:
        """
        Update bump time

        Args:
            timestamp (datetime): Data to write to the file
        """

        self.COLLECTION.update_one(
            self.COLLECTION.find_one(),
            {"$set": {"timestamp": timestamp}}
        )

    def get_bump_time(self) -> datetime.datetime:
        """
        Read timestamp of previous bump 

        Returns:
            datetime.datetime: Most recent bump time
        """

        return self.COLLECTION.find_one()["timestamp"]
