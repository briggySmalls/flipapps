import grpc

from flipdot_assistant.protos.flipapps_pb2_grpc import FlipAppsStub
from flipdot_assistant.protos.flipapps_pb2 import (
    TextRequest, ClockRequest, WeatherRequest)


class FlipAppClient(object):
    def __init__(self):
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = FlipAppsStub(channel)

    def show_text(self, text: str, font: str=None):
        self.stub.Text(TextRequest(text=text, font=font))

    def show_clock(self):
        self.stub.Clock(ClockRequest())

    def show_weather(self, coordinates: tuple):
        self.stub.Weather(WeatherRequest(
            latitude=coordinates[0],
            longitude=coordinates[1]))
