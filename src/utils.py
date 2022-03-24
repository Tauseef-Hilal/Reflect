import datetime

def update_bump_timestamp(timestamp: datetime.datetime) -> None:
    """
    Write new bump time to ../data/reminder.txt

    Args:
        timestamp (datetime): Data to write to the file
    """
    
    with open("data/reminder.txt", "w") as file:
        file.write(str(timestamp))

def get_bump_timestamp() -> datetime.datetime:
    """
    Read timestamp of previous bump from ../data/reminder.txt
    """
    
    with open("data/reminder.txt") as file:
        datetime_str = file.read()
        
    date, time = datetime_str.split()
    
    date = date.split("-")
    date = list(map(int, date))
    
    time = time.replace(".", ":").split(":")
    time = list(map(int, time))
    
    return datetime.datetime(*date, *time)
        