# -*- coding: utf-8 -*-
"""
Utility functions to convert back and forth between a timestring and timedelta.
"""

from django.conf import settings

from datetime import timedelta
import re
from decimal import Decimal

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
    
def timedelta_to_string(value):
    '''
    Renders the given timedelta as string of format "3w 2d 5h 30m."
    '''
    weeks, remainder = divmod(value.total_seconds(), 3600 * HOURS_PER_DAY * DAYS_PER_WEEK)
    days, remainder = divmod(remainder, 3600 * HOURS_PER_DAY)
    hours, remainder = divmod(remainder, 3600)  
    minutes, seconds = divmod(remainder, 60)
    weeks_str = '' 
    days_str = '' 
    hours_str = ''
    minutes_str = ''
    if(weeks > 0):     
        weeks_str = '%dw ' % weeks
    if (days > 0):
        days_str = '%dd ' % days
    if (hours > 0):
        hours_str = '%dh ' % hours
    if (minutes > 0):
        minutes_str = '%dm' % minutes
    time_as_str = weeks_str +  days_str + hours_str + minutes_str
    return time_as_str if not time_as_str == '' else '0h'  

def timedelta_to_decimal(value):
    '''
    Returns the timedelta as decimal object representing the day value.
    
    '''
    return Decimal(value.total_seconds()) / Decimal(3600 * settings.HOURS_PER_DAY) 
    
