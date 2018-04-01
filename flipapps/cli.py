# -*- coding: utf-8 -*-

"""Console script for flipdot_assistant."""
import sys
import argparse

from serial import Serial
from pyflipdot.pyflipdot import HanoverController, HanoverSign
from time import sleep

from flipapps.text_builder import TextBuilder

BAUD_RATE = 4800
ADDRESS = 1
WIDTH = 84
HEIGHT = 7

parser = argparse.ArgumentParser(
    description='Start flipdot command line application')
parser.add_argument(
    'port', type=str, help='Name of serial port to use')


def show_string(controller, text_builder, sign_name, string):
    controller.draw_image(
        text_builder.text_image(string, font_name='silkscreen')[0],
        sign_name=sign_name)

    sleep(3)


def main():
    args = parser.parse_args()

    # Create the controller
    port = Serial(port=args.port, baudrate=BAUD_RATE)
    controller = HanoverController(port)

    # Create and add the sign
    sign = HanoverSign(
        '1',
        address=int(ADDRESS),
        width=int(WIDTH),
        height=int(HEIGHT),
        flip=True)
    controller.add_sign(sign)

    text_builder = TextBuilder(WIDTH, HEIGHT)
    strings = [
        ("Welcome to 438", ""),
        ("Hope you are", "good"),
        ("Please recycle", "")
    ]
    while True:
        for pair in strings:
            show_string(controller, text_builder, '1', pair[0])
            show_string(controller, text_builder, '1', pair[1])

if __name__ == "__main__":
    sys.exit(main())
