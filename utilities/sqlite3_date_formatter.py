import datetime

def convert_to_sqlite3_date(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")

def get_date(datetime_as_str:str)->str:
    """From the database value, gets the only the date as string"""
    
    return datetime_as_str.split(' ')[0]

def get_time(datetime_as_str:str)->str:
    """From the database value, gets the only the time as string"""
    
    return datetime_as_str.split(' ')[1]