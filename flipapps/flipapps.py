# -*- coding: utf-8 -*-

"""Collection of applications for flipdot signs"""
from flipapps.text_builder import TextSign
from pyflipdot.pyflipdot import HanoverController
from serial import Serial
from flipapps.weather import Weather
from flipapps.clock import Clock


class FlipApps(object):
    def __init__(self, port_name: str):
        # Create the controller
        port = Serial(port=port_name)
        self.controller = HanoverController(port)

        # Create the weather app
        self.weather = Weather()

        # Create a clock
        self.clock = Clock()

    def add_sign(self, name: str, address: int, width: int, height: int):
        # Create and add the sign
        sign = TextSign(name, int(address), int(width), int(height), flip=True)
        self.controller.add_sign(sign)

    def write_text(
            self,
            text: str,
            font: str='silkscreen',
            sign_name: str=None):
        self.clock.stop()  # Stop the clock, if it is running
        sign = self._get_sign(sign_name)
        text_image = sign.text_image(text, font)
        self.controller.draw_image(text_image, sign_name=sign.name)

    def show_weather(self, coordinates=None, sign_name: str=None):
        self.clock.stop()  # Stop the clock, if it is running

        # Get the sign and start making an image
        sign = self._get_sign(sign_name)
        image = sign.create_image()

        # Get a weather forecast, and draw an image from it
        forecast = self.weather.get_forecast(coordinates)
        forecast.draw_hourly(image)

        # Send the image to the sign
        self.controller.draw_image(image, sign_name=sign.name)

    def show_clock(self, sign_name: str=None):
        sign = self._get_sign(sign_name)
        self.clock.start(lambda time: self._draw_time(sign, time))

    def _draw_time(self, sign, time):
        time_image = sign.text_image(time, 'nintendo', alignment='centre')
        self.controller.draw_image(time_image, sign_name=sign.name)

    def _get_sign(self, sign_name):
        return self.controller.get_sign(sign_name)
