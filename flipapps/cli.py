# -*- coding: utf-8 -*-

"""Console script for flipdot_assistant."""
import sys
import cmdln
import argparse

from serial import Serial
from pyflipdot.pyflipdot import HanoverController, HanoverSign
import numpy as np

from flipapps.clock import Clock
from flipapps.weather import Weather
from flipapps.writer import Writer
from flipapps.flipapps import AppManager, Request
from flipapps.app import ImageDetails

BAUD_RATE = 4800
ADDRESS = 1
WIDTH = 84
HEIGHT = 7


class FlipdotShell(cmdln.Cmdln):
    intro = "Welcome to the flipdot shell"
    prompt = "(flipdot) "

    def __init__(self, port_name: str):
        # Create the controller
        port = Serial(port=port_name)
        self.controller = HanoverController(port)

        # Create and add the sign
        size = ImageDetails(width=WIDTH, height=HEIGHT)
        sign = HanoverSign(
            'dev',
            address=int(ADDRESS),
            width=int(WIDTH),
            height=int(HEIGHT),
            flip=True)
        self.controller.add_sign(sign)

        # Create the application
        apps = [
            Clock(size, self._draw_image),
            Weather(size, self._draw_image),
            Writer(size, self._draw_image),
        ]
        self.apps = AppManager(apps, 'clock')
        self.apps.start()

        # Do the usual Cmd instantiation
        super().__init__()

    def do_text(
            self,
            subcmd,
            opts,
            text: str,
            font: str = 'silkscreen'):
        assert self.apps.request(
            Request('writer', text=text, font=font))

    def do_weather(
            self,
            subcmd,
            opts,
            latitude: int = None,
            longitude: int = None):
        coordinates = (latitude, longitude) if latitude and longitude else None
        assert self.apps.request(
            Request('weather', coordinates=coordinates))

    def do_clock(self, subcmd, opts):
        assert self.apps.request(Request('clock'))

    def do_stop(self, subcmd, opts):
        self.apps.stop()

    def _draw_image(self, image: np.array):
        self.controller.draw_image(image)

    def _get_sign(self, sign_name: str):
        return self.controller.get_sign(sign_name)


parser = argparse.ArgumentParser(
    description='Start flipdot command line application')
parser.add_argument(
    'port', type=str, help='Name of serial port to use')


def main():
    args = parser.parse_args()
    FlipdotShell(args.port).cmdloop()


if __name__ == "__main__":
    sys.exit(main())
