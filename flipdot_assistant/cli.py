# -*- coding: utf-8 -*-

"""Console script for flipdot_assistant."""
import sys
import click
from cmd import Cmd
# from flipdot_assistant.power import PowerManager
from flipdot_assistant.text_builder import TextBuilder
from pyflipdot.pyflipdot import HanoverSign, HanoverController
from serial import Serial
from PIL import ImageFont

PINS = {
    'pin_sign': 24,
    'pin_lights': 25,
}
BAUD_RATE = 4800
WIDTH = 84
HEIGHT = 7
ADDRESS = 1


class FlipdotShell(Cmd):
    intro = "Welcome to the flipdot shell"
    prompt = "(flipdot)"



@click.group()
def main(args=None):
    """Console script for flipdot_assistant."""
    pass


# @click.command()
# @click.option('state', type=click.Choice(['on', 'off']))
# def lights(state):
#     click.echo("Setting lights state: {}".format(state))
#     power = PowerManager(**PINS)
#     power.lights(state == 'on')


@click.command()
@click.argument('port', type=click.STRING)
@click.argument('address', type=click.INT)
@click.argument('width', type=click.INT)
@click.argument('height', type=click.INT)
@click.argument('text', type=click.STRING)
def write(port, address, width, height, text):
    click.echo("Sending text over {}".format(port))
    # Create the controller
    port = Serial(port=port, baudrate=BAUD_RATE)
    controller = HanoverController(port)

    # Create and add the sign
    sign = HanoverSign('dev', ADDRESS, WIDTH, HEIGHT, flip=True)
    controller.add_sign(sign)

    # Create the text builder
    texter = TextBuilder(WIDTH, HEIGHT)
    # power.lights(state == 'on')


main.add_command(write)


if __name__ == "__main__":
    sys.exit(FlipdotShell.cmdloop())
