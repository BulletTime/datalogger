import logging
import time
import ConfigParser

import Sensors.GPS.GPS as GPS


class Interface:
    settings = ConfigParser.ConfigParser()

    def __init__(self, settings_file):
        self.load_settings(settings_file)
        self.gps = GPS.GPS(debug=self.settings.getboolean('General', 'debug'))

    def load_settings(self, settings_file):
        self.settings.read(settings_file)
        logging.info('Settings read and restored')

    def print_all_settings(self):
        logging.info('Print all settings')
        print('All settings:\n')
        sections = self.settings.sections()
        for section in sections:
            print('Section [%s]' % section)
            items = self.settings.items(section)
            for item in items:
                print('\tOption [%s] : %s' % (item[0], item[1]))

    def start_gps(self):
        logging.info('Start gps')
        # self.gps.setDaemon(True)
        self.gps.start()
        while(True):
            print(self.gps.get_longitude())
            time.sleep(1)

    def cleanup(self):
        logging.info('Cleaning up')
        self.settings = None
        self.gps.cleanup()
        self.gps.join()
