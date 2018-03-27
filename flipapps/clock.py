# -*- coding: utf-8 -*-

"""Simple clock application"""
from datetime import datetime
from threading import Timer


class PeriodicTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)

        self.finished.set()


class Clock(object):
    def __init__(self):
        self.timer = None

    def start(self, callback):
        if self.timer is not None:
            self.stop()

        self.now = datetime.now()
        self.callback = callback
        self.timer = PeriodicTimer(1, self.print_time)
        self.timer.start()

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def print_time(self):
        # Get the current time
        now = datetime.now()
        if self.now == now:
            # We've drifted
            return

        self.callback(now.strftime("%H:%M:%S"))
        self.now = now
