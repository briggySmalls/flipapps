# -*- coding: utf-8 -*-

"""Console script for flipdot_assistant."""
import sys
import cmdln
import argparse
import time
import asyncio

from flipapps.flipapps import FlipApps, Sign

ADDRESS = 1
WIDTH = 84
HEIGHT = 7
MIN_WRITE_INTERVAL_S = 2


class FlipdotShell(cmdln.Cmdln):
    intro = "Welcome to the flipdot shell"
    prompt = "(flipdot) "

    def __init__(self, apps: FlipApps):
        self.apps = apps
        # Do the usual Cmd instantiation
        super().__init__()

    def do_text(
            self,
            subcmd,
            opts,
            text: str,
            font: str = 'silkscreen'):
        self.apps.text(text=text, font=font)

    def do_weather(
            self,
            subcmd,
            opts,
            latitude: int = None,
            longitude: int = None):
        coordinates = (latitude, longitude) if latitude and longitude else None
        self.apps.weather(coordinates)

    def do_clock(self, subcmd, opts):
        self.apps.clock()


parser = argparse.ArgumentParser(
    description='Start flipdot command line application')
parser.add_argument(
    'port', type=str, help='Name of serial port to use')


def main():
    args = parser.parse_args()
    sign = Sign(
        ADDRESS,
        WIDTH,
        HEIGHT,
        flip=True,
        min_write_inteval=MIN_WRITE_INTERVAL_S)
    with FlipApps(args.port, sign) as apps:
        FlipdotShell(apps).cmdloop()


if __name__ == "__main__":
    sys.exit(main())
