from threading import Thread, Event
from time import sleep
from collections import namedtuple
import numpy as np


ImageDetails = namedtuple('ImageDetails', ['width', 'height'])


class App(object,):
    def __init__(self, image_details: ImageDetails, draw_image):
        self.cancel_request = Event()
        self.thread = None
        self.name = self.__class__.__name__.lower()
        self.image_details = image_details
        self.draw_image = draw_image
        self._setup()

    def _setup(self):
        pass

    def start(self, *args, **kwargs):
        self.thread = Thread(
            target=self._run,
            args=args,
            kwargs=kwargs)
        self.cancel_request.clear()
        self.thread.start()

    def stop(self):
        if self.thread is None:
            raise RuntimeError("App was never started")

        # Check if the app is still running
        if not self.is_active:
            return

        # Request the thread to stop
        self.cancel_request.set()
        # Block until thread has stopped
        while self.is_active:
            sleep(0.01)

    @property
    def is_cancel_requested(self):
        return self.cancel_request.is_set()

    @property
    def is_active(self):
        return self.thread.is_alive()

    def _run(self, *args, **kwargs):
        raise NotImplementedError()

    def create_image(self):
        return np.full(
            (self.image_details.height, self.image_details.width), False)
