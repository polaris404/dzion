import re
import asyncio
#from db import get_datetime
from datetime import timedelta

def timetotext(td):
    secs = abs(td.total_seconds())
    text_list = []

    unit_names = {"year": ("year", "years"),
                  "month": ("month", "months"),
                  "week": ("week", "weeks"),
                  "day": ("day", "days"),
                  "hour": ("hour", "hours"),
                  "minute": ("minute", "minutes"),
                  "second": ("second", "seconds")}

    unit_limits = [("year", 365 * 24 * 3600),
                   ("month", 30 * 24 * 3600),
                   ("week", 7 * 24 * 3600),
                   ("day", 24 * 3600),
                   ("hour", 3600),
                   ("minute", 60),
                   ("second", 1)]

    for unit, limit in unit_limits:
        if limit > secs:
            continue
        unit_value = secs // limit
        secs %= limit
        if unit_value == 1:
            text_list.append(f'**{int(unit_value)} {unit_names[unit][0]}**')
        else:
            text_list.append(f'**{int(unit_value)} {unit_names[unit][1]}**')

    if len(text_list) > 1:
        string = ", ".join(text_list[:-1])
        string = string + " and " + text_list[-1]
    else:
        string = text_list[0]

    return string

def time_to_timedelta(string):
    s=0
    m=0
    h=0
    d=0
    if re.search(r'(\d+)[m|M]', string) is not None:
        m = int(re.search(r'(\d+)[m|M]', string).group(1))
    if re.search(r'(\d+)[s|S]', string) is not None:
        s = int(re.search(r'(\d+)[s|S]', string).group(1))
    if re.search(r'(\d+)[h|H]', string) is not None:
        h = int(re.search(r'(\d+)[h|H]', string).group(1))
    if re.search(r'(\d+)[d|D]', string) is not None:
        d = int(re.search(r'(\d+)[d|D]', string).group(1))

    delta = timedelta(days=d, seconds=s, microseconds=0, milliseconds=0, minutes=m, hours=h, weeks=0)
    return delta

def is_valid_time(string):
    match = re.search(r'\d+[dDhHmMsS]', string)
    if match is not None:
        return True
    return False
