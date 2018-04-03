# -*- coding: utf-8 -*-

"""Collection of apps for use with a flipdot sign"""
from collections import namedtuple
import asyncio
import time
from serial import Serial

import numpy as np
from pyflipdot.pyflipdot import HanoverController, HanoverSign

from flipapps.app_manager import AppManager, Request
from flipapps.app import ImageDetails
from flipapps.clock import Clock
from flipapps.weather import Weather
from flipapps.writer import Writer

Sign = namedtuple(
    'Sign',
    ['address', 'width', 'height', 'flip', 'min_write_inteval']
)


def _test_draw(image: np.array):
    test_image = np.full(image.shape, ' ')
    test_image[image] = '#'
    for row in test_image:
        print("|{}|".format(''.join(list(row))))


class FlipApps(object):
    def __init__(self, port_name: str, sign: Sign):
        # Create a controller
        self.port = Serial(port_name)
        self.controller = HanoverController(self.port)

        # Create a sign
        self.sign = HanoverSign(
            '1', sign.address, sign.width, sign.height, sign.flip)
        self.controller.add_sign(self.sign)
        self.min_write_inteval = sign.min_write_inteval

        # Create some apps
        size = ImageDetails(width=sign.width, height=sign.height)
        apps = [
            Clock(size, self._draw_image),
            Weather(size, self._draw_image),
            Writer(size, self._draw_image),
        ]
        self.app_manager = AppManager(apps, 'clock')

        # Initialise some variables
        self.last_draw_time = 0

    def __enter__(self):
        self.app_manager.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.app_manager.__exit__(type, value, traceback)
        self.port.close()

    def start(self):
        self.app_manager.start()

    def stop(self):
        self.app_manager.stop()
        self.port.close()

    def text(self, text, font='silkscreen'):
        self.app_manager.request(
            Request('writer', text=text, font=font))

    def clock(self):
        self.app_manager.request(Request('clock'))

    def weather(self, coordinates=None):
        self.app_manager.request(
            Request('weather', coordinates=coordinates))

    async def _draw_image(self, image: np.array):
        # Ensure we are able to draw
        disparity = time.time() - self.last_draw_time
        if disparity < self.min_write_inteval:
            await asyncio.sleep(disparity)

        # # Draw the image and record the time
        self.controller.draw_image(image)
        self.last_draw_time = time.time()
