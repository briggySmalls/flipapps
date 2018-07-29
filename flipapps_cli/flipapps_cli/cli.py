# -*- coding: utf-8 -*-

"""Console script for flipapps_cli."""
import sys
import click

from client import FlipAppClient


@click.group()
@click.pass_context
def flipapps(ctx):
    """Console script for flipapps_cli."""
    ctx.obj = FlipAppClient()
    return 0


@flipapps.command()
@click.pass_obj
def clock(client):
    """Display the clock"""
    client.show_clock()


@flipapps.command()
@click.option('--font', default=None)
@click.argument('message')
@click.pass_obj
def text(client, message, font):
    """Display the provided message"""
    client.show_text(text=message, font=font)


@flipapps.command()
@click.option('--coordinates', nargs=2, type=float)
@click.pass_obj
def weather(client, coordinates):
    """Display the weather for the provided location"""
    client.show_weather(coordinates)


@flipapps.command()
@click.option('--on/--off')
@click.pass_obj
def lights(client, status):
    """Turn lights on/off"""
    client.power_lights(status)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
