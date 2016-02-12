import time
from Sensors.GPS.GPS import GPS, GPSData
from gps.client import dictwrapper
from nose.tools import assert_equal, assert_not_equal, assert_is_none, assert_true, assert_false, raises


def test_create_debug_session():
    gps = GPS(debug=1)
    assert_equal(gps.host, 'localhost')
    assert_equal(gps.port, '2947')
    assert_true(gps.debug)
    assert_false(gps.exit_flag)
    assert_is_none(gps.session)


@raises(IOError)
def test_create_normal_session():
    GPS()


def test_get_instance():
    gps = GPS(debug=1)
    assert_equal(GPS.get_instance(), gps)
    gps2 = GPS(debug=1)
    assert_equal(GPS.get_instance(), gps2)
    assert_not_equal(GPS.get_instance(), gps)


def test_data_processing():
    gps = GPS(debug=1)
    data = GPSData(dictwrapper({'class': 'TPV', 'time': '2010-04-30T11:48:20.10Z', 'lat': 46.498204497,
                                'lon': 7.568061439, 'alt': 1327.689, 'track': 10.3797, 'speed': 0.091,
                                'climb': -0.085}))
    gps.read()
    assert_equal(gps.get_data(), data)


def test_cleanup():
    gps = GPS(debug=1)
    assert_false(gps.exit_flag)
    gps.cleanup()
    assert_true(gps.exit_flag)


def test_thread():
    gps = GPS(debug=1)
    gps.start()
    time.sleep(.2)
    data = GPSData(dictwrapper({'class': 'TPV', 'time': '2010-04-30T11:48:20.10Z', 'lat': 46.498204497,
                                'lon': 7.568061439, 'alt': 1327.689, 'track': 10.3797, 'speed': 0.091,
                                'climb': -0.085}))
    assert_equal(gps.get_data(), data)
    gps.cleanup()
