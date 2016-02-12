import logging
import time
import sys
from threading import Thread

try:
    import gps
    from gps.client import dictwrapper
except RuntimeError:
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
        if not debug:
            self.session = gps.gps(self.host, self.port)
            self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        else:
            self.session = None
        self.data = GPSData()

    @staticmethod
    def get_instance():
        global instance
        return instance

    def run(self):
        logging.info('Starting %s thread' % self.__class__)
        while not self.exit_flag:
            self.read()
            if self.debug:
                time.sleep(.1)
        logging.info('Closing %s thread' % self.__class__)

    def read(self):
        logging.debug('Reading GPS signal')
        if self.debug:
            self.data = GPSData(dictwrapper({'class': 'TPV', 'time': '2010-04-30T11:48:20.10Z', 'lat': 46.498204497,
                                             'lon': 7.568061439, 'alt': 1327.689, 'track': 10.3797, 'speed': 0.091,
                                             'climb': -0.085}))
        elif not self.debug and self.session.running:
            self.data = GPSData(self.session.next())
            logging.error('The gpsd session isn\'t running')
            sys.exit(1)

    def get_data(self):
        return self.data

    def cleanup(self):
        logging.info('Cleaning up')
        self.exit_flag = True


class GPSData:
    def __init__(self, report=None):
        self._is_valid = False
        if report is not None and 'class' in report and report['class'] == 'TPV':
            if hasattr(report, 'time'):
                self._time = report.time
                self._is_valid = True
            if hasattr(report, 'lat'):
                self._latitude = report.lat
            if hasattr(report, 'lon'):
                self._longitude = report.lon
            if hasattr(report, 'alt'):
                self._altitude = report.alt
            if hasattr(report, 'speed'):
                self._speed = report.speed
            if hasattr(report, 'climb'):
                self._climb = report.climb
            if hasattr(report, 'track'):
                self._track = report.track
        else:
            logging.warning('No gps signal')

    def get_time(self):
        try:
            return self._time
        except AttributeError:
            return None

    def get_latitude(self):
        try:
            return self._latitude
        except AttributeError:
            return None

    def get_longitude(self):
        try:
            return self._longitude
        except AttributeError:
            return None

    def get_altitude(self):
        try:
            return self._altitude
        except AttributeError:
            return None

    def get_speed(self):
        try:
            return self._speed
        except AttributeError:
            return None

    def get_climb(self):
        try:
            return self._climb
        except AttributeError:
            return None

    def get_track(self):
        try:
            return self._track
        except AttributeError:
            return None

    def is_valid(self):
        return self._is_valid

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.__dict__)
    __repr__ = __str__
