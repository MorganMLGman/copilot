""" Basic commands for operation
"""
import logging
import logging.config
from time import time
import datetime as dt
import psutil

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger('copilotLogger')

def get_date() -> dt.datetime:
    """get_date Function to get system date

    Returns:
        date: System date
    """
    return dt.datetime.today()

def get_time() -> dt.datetime:
    """get_time Function to get system time

    Returns:
        time: System time
    """
    return dt.datetime.now().time

def get_datetime() -> dt.datetime:
    """get_datetime Function to get system date and time

    Returns:
        datetime: System date and time
    """
    return dt.datetime.now()

def get_uptime(since: bool) -> str:
    """get_uptime Function to get system uptime

    Args:
        since (bool): If True returns system start date, else time elapsed

    Returns:
        str: Uptime
    """
    boot_time = psutil.boot_time()

    if since:
        return dt.datetime.fromtimestamp(boot_time).strftime("%d/%m/%Y %H:%M:%S")
    return dt.timedelta(seconds=time() - boot_time)
