import logging
import logging.config
import commands

def main():
    logging.config.fileConfig(fname='log.conf', disable_existing_loggers=True)
    logger = logging.getLogger('copilotLogger')
    
    commands.get_swap_stats()
    

if __name__ == "__main__":
    main()