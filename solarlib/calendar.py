import datetime
import pytz

JULIAN_DAYS_INIT = 1721424.5
CENTURY21 = 2451545
CENTURY_DAYS = 36525

def time2seconds(time):
    hour = time.hour
    minute = time.minute
    seconds = time.second
    return hour * 3600 + minute * 60 + seconds


def julian_day(time):
    utc = pytz.timezone('UTC')
    utc_time = time.astimezone(utc)
    time_of_day = time2seconds(utc_time)/3600/24
    return JULIAN_DAYS_INIT + utc_time.toordinal() + time_of_day

def julian_century(time):
    return (julian_day(time)-CENTURY21)/CENTURY_DAYS
    