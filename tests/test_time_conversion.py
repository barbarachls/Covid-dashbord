from time_conversion import minutes_to_seconds
from time_conversion import hours_to_minutes
from time_conversion import hhmm_to_seconds
from time_conversion import current_time_hhmm
from time_conversion import sched_time


def test_minutes_to_seconds():
    seconds = minutes_to_seconds('1')
    assert seconds == 60
    assert isinstance(seconds, int)


def test_hours_to_minutes():
    minutes = hours_to_minutes('1')
    assert minutes == 60
    assert isinstance(minutes, int)


def test_hhmm_to_seconds():
    time = hhmm_to_seconds('01:00')
    assert time == 3600
    assert isinstance(time, int)


def test_current_time():
    time = current_time_hhmm()
    assert (time, str)


def test_sched_time():
    interval = sched_time('10:00')
    assert isinstance(interval, int)
