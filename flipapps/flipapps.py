# -*- coding: utf-8 -*-

"""Collection of applications for flipdot signs"""
from flipapps.app import App
import asyncio
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
        self.idle_app = self.apps[idle_app_name]
        self.loop = None
        # Create application thread
        self.is_cancel_requested = Event()
        self.runner = Thread(target=self._run, name="app-manager")

    def request(self, request: Request):
        self.loop.call_soon_threadsafe(self._change_app, request)

    def start(self):
        self.current_app_task = None
        self.runner.start()

    def stop(self):
        print("Stop called")
        # Post an instruction for the loop to stop
        # This will cause the loop thread to terminate too
        self.loop.call_soon_threadsafe(self.loop.stop)

    def _change_app(self, request: Request):
        # Stop current app
        if self._is_currently_running:
            print("Stopping current app")
            self.current_app_task.cancel()

        # Start requested app
        print("Starting app '{}'".format(request.app))
        # Schedule app's run function to call asynchronously
        self.current_app_task = self.loop.create_task(
            self.apps[request.app].run(*request.args, **request.kwargs))

    def _run(self):
        # Create an async event loop for our applications to run out of
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        self.loop.close()

    @property
    def _is_currently_running(self):
        return self.current_app_task and not self.current_app_task.done()
