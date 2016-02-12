from Sensors.GPS.GPS import GPSData
from gps.client import dictwrapper
from nose.tools import assert_equal, assert_is_none, assert_true, assert_false


def test_empty():
    data = GPSData()
    assert_is_none(data.get_time())
    assert_is_none(data.get_latitude())
    assert_is_none(data.get_longitude())
    assert_is_none(data.get_altitude())
    assert_is_none(data.get_speed())
    assert_is_none(data.get_climb())
    assert_is_none(data.get_track())
    assert_false(data.is_valid())


def test_valid_mock():
    data = GPSData(dictwrapper({'class': 'TPV', 'time': '2010-04-30T11:48:20.10Z', 'lat': 46.498204497,
                                'lon': 7.568061439, 'alt': 1327.689, 'track': 10.3797, 'speed': 0.091,
                                'climb': -0.085}))
    assert_equal(data.get_time(), '2010-04-30T11:48:20.10Z')
    assert_equal(data.get_latitude(), 46.498204497)
    assert_equal(data.get_longitude(), 7.568061439)
    assert_equal(data.get_altitude(), 1327.689)
    assert_equal(data.get_speed(), 0.091)
    assert_equal(data.get_climb(), -0.085)
    assert_equal(data.get_track(), 10.3797)
    assert_true(data.is_valid())


def test_invalid_mock():
    data = GPSData(dictwrapper({'class': 'Wrong', 'time': '2010-04-30T11:48:20.10Z', 'lat': 46.498204497,
                                'lon': 7.568061439, 'alt': 1327.689, 'track': 10.3797, 'speed': 0.091,
                                'climb': -0.085}))
    assert_is_none(data.get_time())
    assert_is_none(data.get_latitude())
    assert_is_none(data.get_longitude())
    assert_is_none(data.get_altitude())
    assert_is_none(data.get_speed())
    assert_is_none(data.get_climb())
    assert_is_none(data.get_track())
    assert_false(data.is_valid())
