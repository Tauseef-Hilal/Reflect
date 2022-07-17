import datetime

from pymongo.database import Database
from pymongo.collection import Collection


class BumpTimer:
    """
    Feature: Bump Reminder
    """

    def update_bump_time(
        self,
        collection: Collection,
        timestamp: datetime.datetime
    ) -> None:
        """
        Update bump time

        Args:
            timestamp (datetime): Bump timestamp
        """

        collection.update_one(
            collection.find_one(),
            {"$set": {"bump_timestamp": timestamp}}
        )

    def get_bump_time(self, collection: Collection) -> datetime.datetime:
        """
        Read timestamp of previous bump 

        Returns:
            datetime.datetime: Most recent bump time
        """

        return collection.find_one()["bump_timestamp"]
