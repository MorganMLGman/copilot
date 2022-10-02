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
    ret = dt.datetime.now().time
    logger.debug(ret)
    return ret

def get_datetime() -> dt.datetime:
    """get_datetime Function to get system date and time

    Returns:
        datetime: System date and time
    """
    ret = dt.datetime.now()
    logger.debug(ret)
    return ret

def get_uptime(since: bool) -> str:
    """get_uptime Function to get system uptime

    Args:
        since (bool): If True returns system start date, else time elapsed

    Returns:
        str: Uptime
    """
    boot_time = psutil.boot_time()
    ret = ""

    if since:
        ret = dt.datetime.fromtimestamp(boot_time).strftime("%d/%m/%Y %H:%M:%S")
    ret = str(dt.timedelta(seconds=time() - boot_time))

    logger.debug(ret)
    return ret

def get_ram_total() -> float:
    """get_ram_total Function te get total ram in system

    Returns:
        float: Total RAM in  GiB
    """
    ret = round(psutil.virtual_memory().total / (2 ** 30), 3)
    logger.debug("Total RAM: %s GiB", ret)
    return ret

def get_ram_used() -> float:
    """get_ram_used Function to get used ram in system

    Returns:
        float: Used RAM in GiB
    """
    ret = round(psutil.virtual_memory().used / (2 ** 30), 3)
    logger.debug("Used RAM: %s GiB", ret)
    return ret

def get_ram_available() -> float:
    """get_ram_available Function to get available ram in system

    Returns:
        float: Available RAM in GiB
    """
    ret = round(psutil.virtual_memory().available / (2 ** 30), 3)
    logger.debug("Available RAM: %s GiB", ret)
    return ret

def get_ram_stats() -> tuple[float, float, float, float]:
    """get_ram_stats Function to get overall stats of system ram

    Returns:
        tuple[float, float, float, float]: RAM stats, [total, used, available, percent]
    """
    vmem =      psutil.virtual_memory()
    total =     round(vmem.total / (2 ** 30), 3)
    used =      round(vmem.used / (2 ** 30), 3)
    available = round(vmem.available / (2 ** 30), 3)
    percent =   vmem.percent

    ret = (total, used, available, percent)

    logger.debug("Stats RAM: %s", ret)

    return ret

def get_swap_total() -> float:
    """get_swap_total Function to get total swap size

    Returns:
        float: Swap total size
    """
    ret = round(psutil.swap_memory().total / (2 ** 30), 3)
    logger.debug("Total swap: %s GiB", ret)
    return ret

def get_swap_used() -> float:
    """get_swap_used Function to get used swap size

    Returns:
        float: Used swap size
    """
    ret = round(psutil.swap_memory().used / (2 ** 30), 3)
    logger.debug("Used swap: %s GiB", ret)
    return ret

def get_swap_available() -> float:
    """get_swap_available Function to get available swap size

    Returns:
        float: Available swap size
    """
    ret = round(psutil.swap_memory().free / (2 ** 30), 3)
    logger.debug("Available swap: %s GiB", ret)
    return ret

def get_swap_stats() -> tuple[float, float, float, float]:
    """get_swap_stats Function to get swap statistics

    Returns:
        tuple[float, float, float, float]: Swap statistics, [total, used, available, percent]
    """
    swap =      psutil.swap_memory()
    total =     round(swap.total / (2 ** 30), 3)
    used =      round(swap.used / (2 ** 30), 3)
    available = round(swap.free / (2 ** 30), 3)
    percent =   swap.percent

    ret = (total, used, available, percent)

    logger.debug("Swap stats: %s", ret)

    return ret
