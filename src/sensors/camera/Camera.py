import logging
import time
from threading import Thread
# noinspection PyUnresolvedReferences
from picamera import PiCamera
# noinspection PyUnresolvedReferences
from picamera.array import PiRGBArray

instance = None


class Camera(Thread):
    last_image = None

    def __init__(self, width=480, height=360):
        global instance
        super(Camera, self).__init__()
        instance = self
        self.exit_flag = False
        self.width = width
        self.height = height
        self.camera = PiCamera()
        # self.camera.resolution = (1024, 768)
        # self.camera.framerate = 30
        # self.camera.iso = 400
        # self.camera.exposure_mode = 'auto'
        # self.camera.awb_mode = 'tungsten'
        # self.camera.meter_mode = 'average'
        # self.camera.exposure_compensation = 3
        time.sleep(1)
        self.stream = PiRGBArray(self.camera, size=(self.width, self.height))

    @staticmethod
    def get_instance():
        global instance
        return instance

    def run(self):
        logging.info('Starting %s thread' % self.__class__)
        while not self.exit_flag:
            self.capture()
        logging.info('Closing %s thread' % self.__class__)

    def capture(self):
        self.stream.seek(0)
        self.camera.capture(self.stream, format='bgr', use_video_port=True, resize=(self.width, self.height))
        self.last_image = self.stream.array

    def cleanup(self):
        logging.info('Cleaning up')
        self.exit_flag = True
        time.sleep(1)
        self.camera.close()
        self.stream.close()
