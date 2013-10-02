# -*- coding: utf-8 -*-
"""
Utility functions to convert back and forth between a timestring and timedelta.
"""

from django.conf import settings

from datetime import timedelta
import re

DAYS_PER_WEEK = getattr(settings, "DAYS_PER_WEEK", 7)
HOURS_PER_DAY = getattr(settings, "HOURS_PER_DAY", 24)
ALLOW_MONTHS = getattr(settings, "DURATIONFIELD_ALLOW_MONTHS", False)
ALLOW_YEARS = getattr(settings, "DURATIONFIELD_ALLOW_YEARS", False)
MONTHS_TO_DAYS = getattr(settings, "DURATIONFIELD_MONTHS_TO_DAYS", 30)
YEARS_TO_DAYS = getattr(settings, "DURATIONFIELD_YEARS_TO_DAYS", 365)

def str_to_timedelta(td_str):
    """
    Returns a timedelta parsed from a string of format "3w 5d 3h 20m". Seconds and microseconds are 
    not supported at this stage.

    Timedelta displays in the format ``3w 5d 3h 20m``.

    Additionally will handle user input in months and years, translating those
    bits into a count of days which is 'close enough'.
    """
    if not td_str:
        return None

    time_format = r"(?:(?P<weeks>\d+)\W*(?:weeks?|w),?)?\W*(?:(?P<days>\d+)\W*(?:days?|d),?)?\W*(?:(?P<hours>\d+)\W*(?:hours?|h),?)?\W*(?:(?P<minutes>\d+)\W*(?:minutes?|m),?)?\W*"
    if ALLOW_MONTHS:
        time_format = r"(?:(?P<months>\d+)\W*(?:months?|M),?)?\W*" + time_format
    if ALLOW_YEARS:
        time_format = r"(?:(?P<years>\d+)\W*(?:years?|Y),?)?\W*" + time_format
    time_matcher = re.compile(time_format)
    time_matches = time_matcher.match(td_str)
    time_groups = time_matches.groupdict()

    for key in time_groups.keys():
        if time_groups[key]:
            time_groups[key] = int(time_groups[key])
        else:
            time_groups[key] = 0

    if "years" in time_groups.keys():
        time_groups["days"] = time_groups["days"] + (time_groups["years"] * YEARS_TO_DAYS)
    if "months" in time_groups.keys():
        time_groups["days"] = time_groups["days"] + (time_groups["months"] * MONTHS_TO_DAYS)
    time_groups["days"] = time_groups["days"] + (time_groups["weeks"] * DAYS_PER_WEEK)
    time_groups["hours"] = time_groups["hours"] + (time_groups["days"] * HOURS_PER_DAY)

    return timedelta(
        days=0, 
        hours=time_groups["hours"],
        minutes=time_groups["minutes"],
        seconds=0,
        microseconds=0)
