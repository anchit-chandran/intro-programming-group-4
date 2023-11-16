import datetime

def convert_to_sqlite3_date(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")