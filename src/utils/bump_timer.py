import datetime


class BumpTimer:
    """
    Feature: Bump Reminder
    """

    running = False

    def update_bump_time(self, timestamp: datetime.datetime) -> None:
        """
        Write new bump time to ../data/reminder.txt

        Args:
            timestamp (datetime): Data to write to the file
        """

        with open("data/reminder.txt", "w") as file:
            file.write(str(timestamp))

    def get_bump_time(self) -> datetime.datetime:
        """
        Read timestamp of previous bump from ../../data/reminder.txt

        Returns:
            datetime.datetime: Most recent bump time
        """

        with open("data/reminder.txt") as file:
            datetime_str = file.read()

        date, time = datetime_str.split()

        date = date.split("-")
        date = list(map(int, date))

        time = time.replace(".", ":").split(":")
        time = list(map(int, time))

        return datetime.datetime(*date, *time)
