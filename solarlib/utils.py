def get_minutes(time):
    hour = time.hour
    minute = time.minute
    second = time.second
    microsecond = time.microsecond
    return hour * 60 + minute + second / 60 + microsecond / 60 / 1e6
