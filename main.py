import logging
import logging.config
from os import path
import commands
import json

import argparse

def main():
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')
    logging.config.fileConfig(log_file_path, disable_existing_loggers=True)
    logger = logging.getLogger('copilotLogger')
    
    sudoPassword: str = ""
    
    parser = argparse.ArgumentParser(description="This is simple command line python script to help you manage your server")
    
    parser.add_argument("--dash", help="Show basic server statistics", action="store_true")
    
    subparsers = parser.add_subparsers(title='subcommands', dest='command')
    
    sub_reboot = subparsers.add_parser("reboot", help="perform system reboot")
    sub_reboot.add_argument("password", help="sudo password, required for reboot command", type=str)
    
    sub_update = subparsers.add_parser("update", help="System update")
    sub_update.add_argument("action", help="check or perform", type=str)
    sub_update.add_argument("password", help="sudo password, required for update command", type=str)
    
    
    args = parser.parse_args()
    
    if args.dash:
        print(json.dumps(commands.refresh_dashboard()))
                       
    if args.command:
        command = args.command
        
        if command == "reboot":
            if args.password != "":
                print(commands.execute_system_reboot(args.password))
            else:
                print(False)
        
        elif command == "update":
            if args.password != "":
                if args.action != "":
                    if args.action == "check":
                        ret = dict()
                        ret["updates"] = commands.get_available_updates(args.password)
                        print(json.dumps(ret))
                    else:
                        print(False)
                else:
                    print(False)
            else:
                print(False)

if __name__ == "__main__":
    main()