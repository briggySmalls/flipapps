# -*- coding: utf-8 -*-

"""Collection of applications for flipdot signs"""
from flipapps.app import App
from pyflipdot.pyflipdot import HanoverController
from serial import Serial
import queue
from time import sleep
from threading import Thread, Event
from flipapps.weather import Weather
from flipapps.clock import Clock
from flipapps.writer import Writer
from collections import namedtuple


Request = namedtuple('Request', ['app_name', 'args', 'kwargs'])


class AppManager(object):
    def __init__(self, apps, idle_app_name=None):
        # Initialise variables
        self.apps = {app.name: app for app in apps}
        self.requests = queue.Queue()
        self.idle_app = self.apps[idle_app_name]
        self.current_app = None
        # Create application thread
        self.is_cancel_requested = Event()
        self.runner = Thread(target=self._run, args=self)

    def request(self, request):
        # Try to put the request into the queue
        try:
            self.requests.put_nowait(request)
            return True
        except queue.Full:
            return False

    def start(self):
        self.current_app = self.idle_app
        self.runner.start()

    def stop(self):
        self.is_cancel_requested.set()

    def _run(self):
        while not self.is_cancel_requested.is_set():
            # Update the app if necessary
            self._handle_request()
            # Wait a bit
            sleep(1)

    def _handle_request(self):
        try:
            # We have a new app request to handle
            request = self.requests.get_nowait()
        except queue.Empty:
            if (self.current_app is None) or (not self.current_app.is_active):
                # We are idle, so use the idle app
                request = Request(self.idle_app.name, None, None)
            else:
                # If we are idle then there is no no app to start
                return

        # Stop current app
        self.current_app.stop()

        # Start requested app
        self.current_app = self.apps[request.app_name]
        self.current_app.start(*request.args, **request.kwargs)
