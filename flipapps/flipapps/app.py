from collections import namedtuple
import numpy as np


ImageDetails = namedtuple('ImageDetails', ['width', 'height'])


class App(object,):
    def __init__(self, image_details: ImageDetails, draw_image):
        self.name = self.__class__.__name__.lower()
        self.image_details = image_details
        self.draw_image = draw_image
        self._setup()

    def _setup(self):
        pass

    async def run(self, *args, **kwargs):
        raise NotImplementedError()

    def create_image(self):
        return np.full(
            (self.image_details.height, self.image_details.width), False)
