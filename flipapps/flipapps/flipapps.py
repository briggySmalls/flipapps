# -*- coding: utf-8 -*-

"""Collection of apps for use with a flipdot sign"""
from collections import namedtuple
from concurrent import futures
import asyncio
from serial import Serial

import sys
import click
import grpc
import numpy as np
from pyflipdot.pyflipdot import HanoverController, HanoverSign

import flipapps.protos.flipapps_pb2 as flipapps_pb2
from flipapps.protos.flipapps_pb2_grpc import (
    FlipAppsServicer, add_FlipAppsServicer_to_server)
from flipapps.app_manager import AppManager, Request
from flipapps.app import ImageDetails
from flipapps.clock import Clock
from flipapps.weather import Weather
from flipapps.writer import Writer


ADDRESS = 1
WIDTH = 84
HEIGHT = 7
MIN_WRITE_INTERVAL_S = 2

Sign = namedtuple(
    'Sign',
    ['address', 'width', 'height', 'flip', 'min_write_inteval']
)


def _test_draw(image: np.array):
    test_image = np.full(image.shape, ' ')
    test_image[image] = '#'
    for row in test_image:
        print("|{}|".format(''.join(list(row))))


class FlipApps(FlipAppsServicer):
    def __init__(self, port_name: str, sign: Sign, loop):
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
        self.app_manager = AppManager(apps, loop, 'clock')

        # Initialise some variables
        self.last_draw_time = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.port.close()

    def stop(self):
        self.port.close()

    def Text(self, request, context):
        self.app_manager.request(
            Request('writer', text=request.text, font=request.font))
        return flipapps_pb2.FlipAppResponse()

    def Clock(self, request, context):
        self.app_manager.request(Request('clock'))
        return flipapps_pb2.FlipAppResponse()

    def Weather(self, request, context):
        self.app_manager.request(Request(
            'weather', coordinates=(request.latitude, request.longitude)))
        return flipapps_pb2.FlipAppResponse()

    async def _draw_image(self, image: np.array):
        _test_draw(image)

    # async def _draw_image(self, image: np.array):
    #     # Ensure we are able to draw
    #     disparity = time.time() - self.last_draw_time
    #     if disparity < self.min_write_inteval:
    #         await asyncio.sleep(disparity)

    #     # # Draw the image and record the time
    #     self.controller.draw_image(image)
    #     self.last_draw_time = time.time()


def serve(flipapps):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_FlipAppsServicer_to_server(flipapps, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    return server


@click.command()
@click.option(
    '--port',
    prompt="The serial port",
    help="The name of the serial port connected to the sign")
def main(port):
    sign = Sign(
        ADDRESS,
        WIDTH,
        HEIGHT,
        flip=True,
        min_write_inteval=MIN_WRITE_INTERVAL_S)
    loop = asyncio.get_event_loop()
    with FlipApps(port, sign, loop) as apps:
        server = serve(apps)
        try:
            while True:
                loop.run_forever()
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == "__main__":
    sys.exit(main())
