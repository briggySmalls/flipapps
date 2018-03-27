# -*- coding: utf-8 -*-

"""Console script for flipdot_assistant."""
import sys
import cmdln
import argparse

from flipapps.flipapps import FlipApps

BAUD_RATE = 4800


class FlipdotShell(cmdln.Cmdln):
    intro = "Welcome to the flipdot shell"
    prompt = "(flipdot) "

    def __init__(self, port_name: str):
        # Create the application
        self.apps = FlipApps(port_name)

        # Do the usual Cmd instantiation
        super().__init__()

    def do_sign(
            self,
            subcmd,
            opts,
            name: str,
            address: int,
            width: int,
            height: int):
        # Create and add the sign
        self.apps.add_sign(name, int(address), int(width), int(height))

    def do_text(
            self,
            subcmd,
            opts,
            text: str,
            font: str = 'silkscreen',
            sign_name: str = None):
        self.apps.write_text(text, font, sign_name)

    def do_weather(
            self,
            subcmd,
            opts,
            latitude: int = None,
            longitude: int = None,
            sign_name: str = None):
        coordinates = (latitude, longitude) if latitude and longitude else None
        self.apps.show_weather(coordinates, sign_name)

    def do_clock(self, subcmd, opts, sign_name: str = None):
        self.apps.show_clock(sign_name)

    def do_test(self, subcmd, opts, sign_name: str = None):
        self.apps.test(sign_name)


parser = argparse.ArgumentParser(
    description='Start flipdot command line application')
parser.add_argument(
    'port', type=str, help='Name of serial port to use')


def main():
    args = parser.parse_args()
    FlipdotShell(args.port).cmdloop()


if __name__ == "__main__":
    sys.exit(main())
