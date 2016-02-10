import logging
import argparse
import time
import threading

import Interface

log_level = 'INFO'


def setup_parser():
    global log_level
    parser = argparse.ArgumentParser(description='starts the data logging program')
    parser.add_argument('-l', '--log', help='indicates the level of logging (WARNING, INFO, DEBUG)')
    args = parser.parse_args()
    if args.log:
        log_level = args.log


def setup_logger():
    global log_level
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(filename='logger.log', level=numeric_level,
                        format='%(asctime)s :: [%(levelname)s] :: %(filename)s :: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')


def setup():
    setup_parser()
    setup_logger()
    logging.info('----------------------------------------')
    logging.info('Starting')
    logging.info('----------------------------------------')
    interface = Interface.Interface('settings.ini')
    try:
        # logging.error('Nothing to run!')
        interface.print_all_settings()
        interface.start_gps()
        while threading.active_count() > 0:
            time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        logging.warning('Interrupted execution')
        interface.cleanup()

    logging.info('----------------------------------------')
    logging.info('Stopping')
    logging.info('----------------------------------------')


if __name__ == "__main__":
    setup()
