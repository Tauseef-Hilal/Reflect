import datetime

from pymongo.collection import Collection


class BumpTimer:
    """
    Feature: Bump Reminder
    """

    def update_bump_time(
        self,
        collection: Collection,
        guild_id: int,
        timestamp: datetime.datetime
    ) -> None:
        """
        Update bump time

        Args:
            timestamp (datetime): Bump timestamp
        """

        collection.update_one(
            collection.find_one({"guild_id": guild_id}),
            {"$set": {"bump_timestamp": timestamp}}
        )

    def get_bump_time(self, data: dict) -> datetime.datetime:
        """
        Read timestamp of previous bump 

        Returns:
            datetime.datetime: Most recent bump time
        """

        return data["bump_timestamp"]
