# -*- coding: utf-8 -*-

"""Collection of applications for flipdot signs"""
from flipapps.app import App
import queue
from time import sleep
from threading import Thread, Event


class Request(object):
    def __init__(self, app: str, *args, **kwargs):
        self.app = app
        self.args = args
        self.kwargs = kwargs


class AppManager(object):
    def __init__(self, apps, idle_app_name: str = None):
        # Initialise variables
        self.apps = {app.name: app for app in apps}
        self.requests = queue.Queue()
        self.idle_app = self.apps[idle_app_name]
        self.current_app = None
        # Create application thread
        self.is_cancel_requested = Event()
        self.runner = Thread(target=self._run)

    def request(self, request: Request):
        # Try to put the request into the queue
        try:
            self.requests.put_nowait(request)
            return True
        except queue.Full:
            return False

    def start(self):
        self.current_app = None
        self.runner.start()

    def stop(self):
        print("Stop called")
        self.current_app.stop()
        self.is_cancel_requested.set()


    def _run(self):
        while not self.is_cancel_requested.is_set():
            print("Iterating...")
            # Update the app if necessary
            self._handle_request()
            # Wait a bit
            sleep(1)

    @property
    def _is_currently_running(self):
        return (self.current_app is not None) and (self.current_app.is_active)

    def _handle_request(self):
        try:
            # We have a new app request to handle
            request = self.requests.get_nowait()
        except queue.Empty:
            if not self._is_currently_running:
                # We are idle, so use the idle app
                request = Request(self.idle_app.name, None, None)
            else:
                return

        # Stop current app
        if self._is_currently_running:
            print("Stopping previous app")
            self.current_app.stop()

        # Start requested app
        print("Starting app '{}'".format(request.app))
        self.current_app = self.apps[request.app]
        self.current_app.start(*request.args, **request.kwargs)
