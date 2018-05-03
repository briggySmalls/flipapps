# -*- coding: utf-8 -*-

"""Collection of apps for use with a flipdot sign"""
from concurrent import futures
import asyncio

import attr
import grpc
import numpy as np

import flipapps.protos.flipapps_pb2 as flipapps_pb2
from flipapps.protos.flipapps_pb2_grpc import (
    FlipAppsServicer, add_FlipAppsServicer_to_server)
from flipapps.app_manager import AppManager, Request
from flipapps.app import ImageDetails
from flipapps.clock import Clock
from flipapps.weather import Weather
from flipapps.writer import Writer


class FlipApps(FlipAppsServicer):
    def __init__(self, image: ImageDetails, callback, loop=None):
        # Ensure we have an event loop to work with
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        # Create some apps
        apps = [
            Clock(image, callback),
            Weather(image, callback),
            Writer(image, callback),
        ]

        # Add the apps to a manager
        self.app_manager = AppManager(apps, self.loop, 'clock')

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

    def run(self):
        # Start the gRPC server (threaded)
        server = self._serve()

        # Run until the user interrupts
        try:
            while True:
                # Handle incoming
                self.loop.run_forever()
        except KeyboardInterrupt:
            # Stop the server and return
            server.stop(0)

    def _serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_FlipAppsServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        return server
