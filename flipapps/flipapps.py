# -*- coding: utf-8 -*-

"""Collection of applications for flipdot signs"""
from flipapps.app import App
import asyncio
from time import sleep
import queue
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
        self.loop = None
        # Create application thread
        self.is_cancel_requested = Event()
        self.runner = Thread(target=self._run, name="app-manager")

    def request(self, request: Request):
        # Try to put the request into the queue
        try:
            self.requests.put_nowait(request)
            return True
        except queue.Full:
            return False

    def start(self):
        self.current_app_task = None
        self.runner.start()

    def stop(self):
        print("Stop called")
        # Post an instruction for the loop to stop
        # This will cause the loop thread to terminate too
        self.loop.call_soon_threadsafe(self.loop.stop)

    async def _run_request_listener(self):
        while True:
            # Wait for a request to come in
            await self._handle_request()
            # Wait a bit
            asyncio.sleep(1)

    async def _handle_request(self):
        try:
            # We have a new app request to handle
            request = self.requests.get_nowait()
        except queue.Empty:
            return

        # Stop current app
        if self._is_currently_running:
            print("Stopping current app")
            self.current_app_task.cancel()

        async def _run_app():
            await self.apps[request.app]._run(*request.args, **request.kwargs)

        # Start requested app
        print("Starting app '{}'".format(request.app))
        # Schedule app's run function to call asynchronously
        self.current_app_task = _run_app

    async def _run_app(self):
        print("Running")
        while True:
            if self._is_currently_running:
                await self.current_app_task()

    def _run(self):
        # Create an async event loop for our applications to run out of
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(asyncio.gather(
            self._run_app(),
            self._run_request_listener(),
        ))
        self.loop.close()

    @property
    def _is_currently_running(self):
        return self.current_app_task and not self.current_app_task.done()
