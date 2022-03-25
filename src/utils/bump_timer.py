import datetime


class BumpTimer:
    """
    Feature: Bump Reminder
    """

    running = False

    def update_bump_time(self, timestamp: datetime.datetime) -> None:
        """
        Write new bump time to /data/reminder.txt

        Args:
            timestamp (datetime): Data to write to the file
        """

        # Write timestamp to /data/reminder.txt
        with open("data/reminder.txt", "w") as file:
            file.write(str(timestamp))

    def get_bump_time(self) -> datetime.datetime:
        """
        Read timestamp of previous bump from /data/reminder.txt

        Returns:
            datetime.datetime: Most recent bump time
        """

        # Read timestamp from /data/reminder.txt
        with open("data/reminder.txt") as file:
            datetime_str = file.read()

        # Separate date and time
        date, time = datetime_str.split()

        # Create a list containing year, month and day
        date = date.split("-")
        date = list(map(int, date))

        # Create a list containing hour, minute, second, microsecond
        time = time.replace(".", ":").split(":")
        time = list(map(int, time))

        return datetime.datetime(*date, *time)
