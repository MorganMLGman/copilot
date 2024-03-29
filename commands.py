""" Basic commands for operation
"""
import logging
import logging.config
from os.path import exists as os_exists
from os import path
from time import time
import datetime as dt
import psutil
from psutil._common import bytes2human
from shlex import split as xsplit
import subprocess as sproc
import json

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=True)
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
    else:
        ret = str(dt.timedelta(seconds=time() - boot_time)).split(".")[0]

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

def get_swap_stats() -> dict:
    
    ret = dict()
    
    swap =      psutil.swap_memory()
    ret["total"] = bytes2human(swap.total)
    ret["used"] = bytes2human(swap.used)
    ret["free"] = bytes2human(swap.free)
    ret["percent"] = swap.percent

    logger.debug("Swap stats: %s", ret)

    return ret

def get_cpu_cores() -> int:
    """get_cpu_cores Function to get cpu physical core count

    Returns:
        int: cpu physical core count
    """
    ret = psutil.cpu_count(logical=False)

    logger.debug("CPU core count: %s", ret)

    return ret

def get_cpu_threads() -> int:
    """get_cpu_threads Function to get cpu logical core count

    Returns:
        int: cpu logical core count
    """
    ret = psutil.cpu_count(logical=True)

    logger.debug("CPU threads: %s", ret)

    return ret

def get_cpu_max_freq() -> float:
    """get_cpu_max_freq Function to get cpu max frequency

    Returns:
        float: cpu max frequency in MHz
    """
    ret = psutil.cpu_freq().max

    logger.debug("CPU max freq: %s MHz", ret)

    return ret

def get_cpu_min_freq() -> float:
    """get_cpu_min_freq Function to get cpu min frequency

    Returns:
        float: cpu min frequency
    """
    ret = psutil.cpu_freq().min

    logger.debug("CPU min freq: %s MHz", ret)

    return ret

def get_cpu_freq(percore: bool) -> list:
    """get_cpu_freq Function to get cpu current frequency

    Args:
        percore (bool): Get current frequency per cpu core

    Returns:
        list: list of cpu frequency, one item or more if percpu is set
    """
    ret = []

    if percore:
        for core in psutil.cpu_freq(percpu=True):
            ret.append(core.current)
    else:
        ret = psutil.cpu_freq(percpu=False).current

    logger.debug("CPU freq: %s MHz", ret)

    return ret

def get_cpu_usage() -> float:
    ret = psutil.cpu_percent(interval = 1)

    logger.debug("CPU usage: %s %", ret)

    return ret

def get_system_load(percent: bool = False) -> tuple[float, float, float]:
    """get_system_load Function to get system average load over 1 minute, 5 minutes and 15 minutes

    Args:
        percent (bool): Get system load as percent

    Returns:
        tuple[float, float, float]: system load
    """
    ret = ()
    load = psutil.getloadavg()

    if percent:
        ret = tuple(round(x / psutil.cpu_count() * 100, 3) for x in load)
    else:
        ret = tuple(round(x, 3) for x in load)

    logger.debug("System load: %s", ret)

    return ret

def get_cpu_temp(percore: bool = False) -> dict:
    """get_cpu_temp Function to get CPU temperature

    Args:
        percore (bool): Read cpu temperature per core

    Returns:
        list: cpu temperature list, consist of pairs (str, float)
    """
    ret = dict()
    package_temp = []
    core_temp = []
    out = psutil.sensors_temperatures()    
    keys = out.keys()
    
    if len(keys) < 1:
        return ret
    
    is_valid_key = False
    
    for key in keys:
        if (key.lower().find("cpu") != -1) or (key.lower().find("core") != -1) or (key.lower().find("cpu_thermal") != -1) or (key.lower().find("k10temp") != -1) :
            is_valid_key = True
            break
    
    if not is_valid_key:
        return ret

    for sensor in out[key]:
        if sensor.label.lower().find("package") != -1:
            package_temp.append(round(sensor.current, 1))
        
        elif sensor.label.lower().find("core") != -1:
            core_temp.append(round(sensor.current, 1))

        elif sensor.label.lower().find("k10temp") != -1:
            core_temp.append(round(sensor.current, 1))
            

    if len(package_temp) == 0 and len(core_temp) == 0:
        for sensor in out[key]:
            core_temp.append(round(sensor.current, 1))

    if percore:
        if len(package_temp) > 0:
            ret["package"] = package_temp
            
        if len(core_temp) > 0:
            ret["core"] = core_temp
        
    else:
        if package_temp:
            package_temp_avr = sum(x for x in package_temp) / len(package_temp)
            ret["package"] =  round(package_temp_avr, 1)
            
        if core_temp:
            core_temp_avr = sum(x for x in core_temp) / len(core_temp)
            ret["core"] = round(core_temp_avr, 1)
        
    logger.debug("CPU temp: %s", ret)
    
    return ret
    
def get_temp_sensors() -> list:
    """get_temp_sensors Function to get all available temeprature sensors in system

    Returns:
        list: list of sensors
    """
    ret = []
    out = psutil.sensors_temperatures()
    keys = out.keys()
    
    for key in keys:
        if len(out[key]) > 1:
            ret.append((key, len(out[key])))
            
        else:
            ret.append((key, 1))
            
    logger.debug("Available temp sensors: %s", ret)
    
    return ret
    
def get_temp_by_sensor(sensor: str) -> list:
    """get_temp_by_sensor Function to read temperature by specific sensor

    Args:
        sensor (str): sensor name

    Returns:
        list: temperature values
    """
    ret = []
    out = psutil.sensors_temperatures()
    keys = out.keys()
    
    if sensor in keys:
        probes = out[sensor]
        
        for probe in probes:
            ret.append((probe.label, probe.current))
            
        logger.debug("%s probes: %s", sensor, ret)
        return ret
    
    logger.error("Sensor: %s is not available", sensor)
    return None        
    

def get_available_updates(password: str) -> list:
    """get_available_updates Function to check available updates on server

    Returns:
        list: list containing available packets updates
    """
    ret = []
    
    command_echo = xsplit(f"""echo "{password}" """)
    echo_proc = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = echo_proc.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
    
    command = xsplit("sudo -S apt update")
    proc = sproc.Popen( command,
                        stdin=echo_proc.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break


    command = xsplit("sudo -S apt list --upgradable")
    proc = sproc.Popen( command,
                        stdin=echo_proc.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break    

    for line in proc.stdout.readlines()[1::]:
        line_split = line.strip().split(" ")
        ret.append(line_split[0] + ": " + line_split[-1][0:-1:] + " -> " + line_split[1])
        
    if ret is not None:
        logger.debug("Update list generated")
        logger.debug("Update list: %s" % ret)
        return ret
    else:
        logger.error("Update list not generated")
        return None
    
def execute_available_updates(password: str) -> int:
    command_echo = xsplit(f"""echo "{password}" """)
    echo_proc = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = echo_proc.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return 0
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
        
    command = xsplit("sudo -S apt upgrade -y")
    proc = sproc.Popen( command,
                        stdin=echo_proc.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return 0

        else:
            logger.debug("Command %s ended with success" % command)
            break
    
    out = proc.stdout.readlines()[-1].strip().split(" ")[0]
    logger.debug("%s packages updated" % out)
    
    return out

def execute_system_reboot(password: str) -> bool:
    """execute_system_reboot Funtion to execute full system reboot
    """
    
    command_echo = xsplit(f"""echo "{password}" """)
    proc = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
    
    
    command_reboot = xsplit("sudo -S reboot now")
    proc = sproc.Popen( command_reboot,
                        stdin=proc.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_reboot)
            return False
        else:
            logger.debug("Command %s ended with success" % command_reboot)
            break
    
    return True
        
def execute_system_shutdown(password: str) -> None:
    """execute_system_shutdown Function to execute full system shutdown
    """
    command_echo = xsplit(f"""echo "{password}" """)
    proc = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
    
    
    command_shutdown = xsplit("sudo -S shutdown now")
    proc = sproc.Popen( command_shutdown,
                        stdin=proc.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_shutdown)
            return False
        else:
            logger.debug("Command %s ended with success" % command_shutdown)
            break
    
    return True
    
def get_public_ip() -> str:
    """get_public_ip Function to get public IP

    Returns:
        str: public ipv4
    """
    
    command = xsplit("curl ifconfig.me")
    
    proc = sproc.Popen( command,
                        stdin=sproc.PIPE,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break 
        
    #logger.debug("Public IP: %s" % proc.stdout.readline().strip())    
    return proc.stdout.readline().strip()

def get_local_ip() -> str:
    """get_public_ip Function to get public IP

    Returns:
        str: public ipv4
    """
    
    command = xsplit("hostname -I")
    
    proc = sproc.Popen( command,
                        stdin=sproc.PIPE,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break 
        
    #logger.debug("Public IP: %s" % proc.stdout.readline().strip())    
    return proc.stdout.readline().strip().split()[0]

def get_first_proc_by_cpu() -> str:
    """get_first_proc_by_cpu Function to get most cpu demanding process

    Returns:
        str: process name
    """
    ret = ""
    command = xsplit("top -b -n 1")
    proc_top = sproc.Popen( command,
                        stdin=sproc.PIPE,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc_top.poll()
        if return_code is None:
            continue
        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None
        else:
            logger.debug("Command %s ended with success" % command)
            break
        
    command = xsplit("head -n 8")
    proc_head = sproc.Popen( command,
                        stdin=proc_top.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc_head.poll()
        if return_code is None:
            continue
        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None
        else:
            logger.debug("Command %s ended with success" % command)
            break
        
    command = xsplit("tail -n 1")
    proc_tail = sproc.Popen( command,
                        stdin=proc_head.stdout,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc_head.poll()
        if return_code is None:
            continue
        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None
        else:
            logger.debug("Command %s ended with success" % command)
            break
    
    
    out = proc_tail.stdout.readline().strip()
        
    if out and out != "":
        index = len(out) - 1
        
        while not(out[index - 1].isnumeric() and out[index] == " "):
            index -= 1
            
        ret = out[index + 1::]
    
    
    return ret

def get_kernel_version() ->str:
    command = xsplit("uname -r")
    proc = sproc.Popen( command,
                        stdin=sproc.PIPE,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break
        
    return proc.stdout.readline().strip()


def get_hostname() ->str:
    command = xsplit("hostname")
    proc = sproc.Popen( command,
                        stdin=sproc.PIPE,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break
        
    return proc.stdout.readline().strip()

def get_disk_usage(path: str) -> dict:
    ret = {
        "total": 0,
        "used": 0,
        "free": 0,
        "percent": 0,
    }
    
    if os_exists(path):
        out = psutil.disk_usage(path)
        
        ret["total"] = bytes2human(out.total)
        ret["used"] = bytes2human(out.used)
        ret["free"] = bytes2human(out.free)
        ret["percent"] = out.percent
        
    return ret

def get_disk_name(mountpoint: str) -> str:
    ret = ""
    
    command = xsplit("lsblk -J  -o NAME,MOUNTPOINT,MODEL")
    proc = sproc.Popen( command,
                        stdin=sproc.PIPE,
                        stdout=sproc.PIPE,
                        stderr=sproc.PIPE,
                        encoding="utf-8",)

    while True:
        return_code = proc.poll()

        if return_code is None:
            continue

        if return_code == 1:
            logger.error("Command %s not ended successfully" % command)
            return None

        else:
            logger.debug("Command %s ended with success" % command)
            break
    
    devices = json.load(proc.stdout)["blockdevices"]
    
    for device in devices:
        if device["children"]:
            for children in device["children"]:
                if type(children) is dict:
                    if children["mountpoint"] == mountpoint:
                        if children["model"]:
                            ret = device["model"]
                        else:
                            ret = device["name"]
                        break
        
        if ret != "":
            break
        
    return ret

def get_installed_packages() -> int:
    ret = 0
    
    out = sproc.getoutput("dpkg -l | grep -c '^ii'")    
    
    if out != "":
        try:
            ret = int(out)
        except:
            ret = 0     
    return ret

def get_docker_containers(password: str) -> str:
    ret = dict()
    
    command_echo = xsplit(f"""echo "{password}" """)
    proc_echo = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_echo.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
    
    command_docker = xsplit("""sudo -S docker ps -a --format \"{{.Names}} {{.State}} {{.RunningFor}}\" """)
    proc_docker = sproc.Popen(command_docker,
                       stdin=proc_echo.stdout,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_docker.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_docker)
            return False
        else:
            logger.debug("Command %s ended with success" % command_docker)
            break
        
    lines = proc_docker.stdout.readlines()
    
    containers = []
    
    for line in lines:
        line = line.strip()
        items = line.split(" ")
        name = items[0]
        state = items[1]
        runtime = " ".join(items[2:])
        container = {
            "name": name,
            "state": state,
            "runtime": runtime,
        }
        containers.append(container)
    
    containers = sorted(containers, key=lambda item: item["name"])    
    
    ret = {
        "containers": containers,
        "items": len(containers),
    }
    
    return json.dumps(ret)


def execute_container_start(password: str, container: str) -> bool:
    command_echo = xsplit(f"""echo "{password}" """)
    proc_echo = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_echo.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
        
    command_docker = xsplit(f"sudo -S docker start {container}")
    proc_docker = sproc.Popen(command_docker,
                       stdin=proc_echo.stdout,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_docker.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_docker)
            return False
        else:
            logger.debug("Command %s ended with success" % command_docker)
            break
        
    output = proc_docker.stdout.readlines()
    
    if output[0].strip().lower() == container.lower():
        return True
    
    return False
        
    
def execute_container_stop(password: str, container: str) -> bool:
    command_echo = xsplit(f"""echo "{password}" """)
    proc_echo = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_echo.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
        
    command_docker = xsplit(f"sudo -S docker stop {container}")
    proc_docker = sproc.Popen(command_docker,
                       stdin=proc_echo.stdout,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_docker.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_docker)
            return False
        else:
            logger.debug("Command %s ended with success" % command_docker)
            break
        
    output = proc_docker.stdout.readlines()
    
    if output[0].strip().lower() == container.lower():
        return True
    
    return False


def execute_container_restart(password: str, container: str) -> bool:
    command_echo = xsplit(f"""echo "{password}" """)
    proc_echo = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_echo.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
        
    command_docker = xsplit(f"sudo -S docker restart {container}")
    proc_docker = sproc.Popen(command_docker,
                       stdin=proc_echo.stdout,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_docker.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_docker)
            return False
        else:
            logger.debug("Command %s ended with success" % command_docker)
            break
        
    output = proc_docker.stdout.readlines()
    
    if output[0].strip().lower() == container.lower():
        return True
    
    return False


def get_container_stats(password: str, container: str) -> str:
    command_echo = xsplit(f"""echo "{password}" """)
    proc_echo = sproc.Popen(command_echo,
                       stdin=sproc.PIPE,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_echo.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_echo)
            return False
        else:
            logger.debug("Command %s ended with success" % command_echo)
            break
        
    command_docker = xsplit(""" sudo -S docker stats --no-stream --format "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.NetIO}}|{{.BlockIO}}" """)
    proc_docker = sproc.Popen(command_docker,
                       stdin=proc_echo.stdout,
                       stdout=sproc.PIPE,
                       stderr=sproc.PIPE,
                       encoding="utf-8")
    
    while True:
        return_code = proc_docker.poll()
        
        if return_code is None: continue
        elif return_code == 1:
            logger.error("Command %s not ended successfully" % command_docker)
            return False
        else:
            logger.debug("Command %s ended with success" % command_docker)
            break
        
    output = proc_docker.stdout.readlines()
    
    proper_line = ""
        
    for line in output:
        if(line.find(container.lower()) != -1):
            proper_line = line.strip()
            break
        
    if proper_line == "":
        return False
    
    proper_line = proper_line.split("|")
    
    stats  = {
        "name": proper_line[0],
        "cpu": proper_line[1],
        "ram": proper_line[2],
        "net_io": proper_line[3],
        "disk_io": proper_line[4],
    }
    
    ret = json.dumps(stats)
    
    return ret
        
    
def refresh_dashboard() -> dict:
    
    # CPU temp
    # CPU usage
    # RAM usage
    # Kernel version
    # Hostname
    # Uptime
    # Uptime since
    # Stress app
    # Public IP
    # Local IP
    # Packages
        
    ret = dict()    
       
    try:
        ret["cpu_temp"] = str(f"""{get_cpu_temp(False)["core"]} 'C""")
    except KeyError:
        pass
    
    ret["cpu_usage"] = str(f"{psutil.cpu_percent(interval = 1)}%")
    
    ret["ram_usage"] = str(f"{psutil.virtual_memory().percent}%")
    
    ret["swap_usage"] = str(f"{psutil.swap_memory().percent}%")
    
    ret["disk_usage"] = str(f"""{get_disk_usage("/")["percent"]}%""")
    
    ret["disk_name"] = get_disk_name("/")
    
    ret['kernel'] = get_kernel_version()
    
    ret["hostname"] = get_hostname()
    
    ret["uptime"] = get_uptime(False)
    
    ret["uptime_since"] = get_uptime(True)
    
    ret["stress_app"] = get_first_proc_by_cpu()
    
    ret["public_ip"] = get_public_ip()
    
    ret["local_ip"] = get_local_ip()
    
    ret["packages"] = str(get_installed_packages())
    
    return ret
        
        
        
        
