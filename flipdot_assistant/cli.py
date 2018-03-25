# -*- coding: utf-8 -*-

"""Console script for flipdot_assistant."""
import sys
import cmdln
import argparse
from flipdot_assistant.text_builder import TextSign
from pyflipdot.pyflipdot import HanoverController
from serial import Serial
from flipdot_assistant.weather import Weather
from flipdot_assistant.clock import Clock

BAUD_RATE = 4800


def preview_image(image):

    def bit_to_char(image, col, row):
        if image[row, col]:
            return '#'
        return ' '

    (rows, columns) = image.shape
    print("Printing {}x{} image".format(columns, rows))
    for row in range(rows):
        print("|{}|".format(''.join(
            [bit_to_char(image, col, row) for col in range(columns)])))


class FlipdotShell(cmdln.Cmdln):
    intro = "Welcome to the flipdot shell"
    prompt = "(flipdot) "

    def __init__(self, port_name: str):
        # Create the controller
        port = Serial(port=port_name, baudrate=BAUD_RATE)
        self.controller = HanoverController(port)

        # Create the weather app
        self.weather = Weather()

        # Create a clock
        self.clock = Clock()

        # Do the usual Cmd instantiation
        super().__init__()

    def do_sign(self, subcmd, opts, name: str, address: int, width: int, height: int):
        # Create and add the sign
        sign = TextSign(name, int(address), int(width), int(height), flip=True)
        self.controller.add_sign(sign)

    def do_text(
            self,
            subcmd,
            opts,
            text: str,
            font: str='silkscreen',
            sign_name: str=None):
        print("Sending '{}'".format(text))
        sign = self.get_sign(sign_name)
        text_image = sign.text_image(text, font)
        preview_image(text_image)
        self.controller.draw_image(text_image)

    def do_weather(self, subcmd, opts, latitude=None, longitude=None, sign_name: str=None):
        # Get the sign and start making an image
        sign = self.get_sign(sign_name)
        image = sign.create_image()

        # Get a weather forecast, and draw an image from it
        forecast = self.weather.get_forecast(
            (latitude, longitude) if latitude is not None else None)
        forecast.draw_hourly(image)

        # Send the image to the sign
        self.controller.draw_image(image)

    def do_clock(self, subcmd, opts, sign_name: str=None):
        sign = self.get_sign(sign_name)
        self.clock.start(lambda time: self.draw_time(sign, time))

    def draw_time(self, sign, time):
        time_image = sign.text_image(time, 'nintendo', alignment='centre')
        self.controller.draw_image(time_image)

    def get_sign(self, sign_name):
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
