# Datalogger

Please contact <sven.agneessens@gmail.com> when you encounter bugs or have
any questions.


## Dependencies

- Python2
- virtualenv
- gpsd gpsd-clients python-gps

## Installation

* `cd` to the top-level directory
* `virtualenv .`
* `bin/pip install nose`
* `sudo apt-get install gpsd gpsd-clients python-gps`

Depending on your Python version, you might have to invoke `virtualenv2` and
`bin/pip2`.

Alternatively, you can install the nose Python (2.7) libraries via your package manager, 
in which case you don't need virtualenv (you can also drop the bin/ prefix in this case).


## Running

Invoke the server in the top-level directory as such:

    bin/python Logger.py

Pass `--log=LEVEL` if you wish to override the default logging level {WARNING, INFO, DEBUG}.

Depending on your Python version, you might have to invoke `bin/python2`.

## Testing

Invoke the testsuite in the top-level directory as such:

    bin/nosetests

## External Links

* [GPS Module](https://www.adafruit.com/products/746)
* [GPS Tutorial](https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/introduction)
