import logging
import time
import sys
from threading import Thread

try:
    import gps
except ImportError:
    print('Library not installed: python-gps; To install: sudo apt-get install python-gps')

instance = None


class GPS(Thread):
    def __init__(self, host="localhost", port="2947", debug=0):
        global instance
        super(GPS, self).__init__()
        instance = self
        self.exit_flag = False
        self.host = host
        self.port = port
        self.debug = debug
        if 'gps' not in sys.modules:
            logging.warning('Library not installed: python-gps; To install: sudo apt-get install python-gps')
            logging.warning('GPS debug is enabled by lack of library')
            self.debug = 1
        if not debug:
            self.session = gps.gps(self.host, self.port)
            self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        else:
            self.session = None
        self.report = {'class': 'TPV'}

    @staticmethod
    def get_instance():
        global instance
        return instance

    def run(self):
        logging.info('Starting %s thread' % self.__class__)
        while not self.exit_flag:
            self.read()
            if self.debug:
                time.sleep(1)
        logging.info('Closing %s thread' % self.__class__)

    def read(self):
        logging.debug('Reading GPS signal')
        if self.debug:
            self.report = {'class': 'TPV', 'time': '2010-04-30T11:48:20.10Z', 'lat': 46.498204497, 'lon': 7.568061439,
                           'alt': 1327.689, 'track': 10.3797, 'speed': 0.091, 'climb': -0.085}
        elif not self.debug and self.session.running:
            self.report = self.session.next()
        elif not self.debug and not self.session.running:
            logging.error('The gpsd session isn\'t running')
            sys.exit(1)

    def get_all(self):
        if self.report['class'] == 'TPV':
            return self.report

    def get_time(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'time'):
                return self.report.time
            if self.debug and 'time' in self.report:
                return self.report['time']

    def get_latitude(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'lat'):
                return self.report.lat
            if self.debug and 'lat' in self.report:
                return self.report['lat']

    def get_longitude(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'lon'):
                return self.report.lon
            if self.debug and 'lon' in self.report:
                return self.report['lon']

    def get_altitude(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'alt'):
                return self.report.alt
            if self.debug and 'alt' in self.report:
                return self.report['alt']

    def get_speed(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'speed'):
                return self.report.speed
            if self.debug and 'speed' in self.report:
                return self.report['speed']

    def get_climb(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'climb'):
                return self.report.climb
            if self.debug and 'climb' in self.report:
                return self.report['climb']

    def get_track(self):
        if self.report['class'] == 'TPV':
            if hasattr(self.report, 'track'):
                return self.report.track
            if self.debug and 'track' in self.report:
                return self.report['track']

    def cleanup(self):
        logging.info('Cleaning up')
        self.exit_flag = True
