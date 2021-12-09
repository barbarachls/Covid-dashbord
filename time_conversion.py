"""Converts time into seconds to then find interval between the current
time and the update time
"""
import time


def minutes_to_seconds(minutes: str) -> int:
    """Converts minutes to seconds"""
    return int(minutes) * 60


def hours_to_minutes(hours: str) -> int:
    """Converts hours to minutes"""
    return int(hours) * 60


def hhmm_to_seconds(hhmm: str) -> int:
    """Converts hours and minute to seconds"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
           minutes_to_seconds(hhmm.split(':')[1])


def current_time_hhmm() -> str:
    """Return the current time."""
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)


def sched_time(update_time) -> int:
    """ Return interval between the current time and the update time in
    seconds
    """
    current_time_ss = hhmm_to_seconds(current_time_hhmm())
    update = hhmm_to_seconds(update_time)
    interval = update-current_time_ss
    return interval
