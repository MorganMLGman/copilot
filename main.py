import logging
import logging.config
import commands
import json

import argparse

def main():
    logging.config.fileConfig(fname='~/copilot/log.conf', disable_existing_loggers=True)
    logger = logging.getLogger('copilotLogger')
    
    parser = argparse.ArgumentParser(description="This is simple command line python script to help you manage your server")
    
    parser.add_argument("--dash", help="Show basic server statistics", action="store_true")
    
    subparsers = parser.add_subparsers()
    
    sub_cpu = subparsers.add_parser('cpu', help="Commands related to CPU")
    
    cpu_map = {
        "cores": "Show core count",
        "threads": "Show thread count",
        "freq": "Show current frequency",
        "max_freq": "Show max frequency",
        "min_freq": "Show min frequency",
        "temp": "Show core temperature",
    }
    
    sub_cpu.add_argument("command", choices=cpu_map, help=str(cpu_map))
    sub_cpu.add_argument("--percore", help="Show stats per core", action='store_true')
    
    args = parser.parse_args()
    
    ret = None
    
    if args.dash:
        ret = commands.refresh_dashboard()
    elif args.command == "cores":
        ret = commands.get_cpu_cores()
    elif args.command == "threads":
        ret = commands.get_cpu_threads()
    elif args.command == "freq":
        if args.percore:
            ret = commands.get_cpu_freq(True)
        else:
            ret = commands.get_cpu_freq(False)
    elif args.command == "max_freq":
        ret = commands.get_cpu_max_freq()
    elif args.command == "min_freq":
        ret = commands.get_cpu_min_freq()
    elif args.command == "temp":
        if args.percore:
            ret = commands.get_cpu_temp(True)
        else:
            ret = commands.get_cpu_temp(False)
                        
                        
    if ret:
        out = json.dumps(ret)
        print(out)

if __name__ == "__main__":
    main()