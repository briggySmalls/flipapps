# -*- coding: utf-8 -*-

"""Manager for coordinating apps"""
import asyncio


class Request(object):
    def __init__(self, app: str, *args, **kwargs):
        self.app = app
        self.args = args
        self.kwargs = kwargs


class AppManager(object):
    def __init__(self, apps, loop, idle_app_name: str = None):
        # Initialise variables
        self.apps = {app.name: app for app in apps}
        self.idle_app = self.apps[idle_app_name]
        self.loop = loop
        self.current_app_task = None
        self.loop.create_task(self._run_idle_app())

    def request(self, request: Request):
        self.loop.call_soon_threadsafe(self._change_app, request)

    def _change_app(self, request: Request):
        # Stop current app
        if self._is_currently_running:
            print("Stopping current app")
            self.current_app_task.cancel()

        # Start requested app
        print("Starting app '{}'".format(request.app))

        # Run the requested app
        self.current_app_task = self.loop.create_task(
            self.apps[request.app].run(*request.args, **request.kwargs))

    async def _run_idle_app(self):
        while True:
            if not self._is_currently_running:
                self.current_app_task = self.loop.create_task(
                    self.idle_app.run())
            await asyncio.sleep(1)

    @property
    def _is_currently_running(self):
        return self.current_app_task and not self.current_app_task.done()
