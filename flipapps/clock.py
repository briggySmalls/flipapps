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
        self.timer = PeriodicTimer(1, self.print_time)

    def start(self, callback):
        self.now = datetime.now()
        self.callback = callback
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def print_time(self):
        # Get the current time
        now = datetime.now()
        if self.now == now:
            # We've drifted
            return

        self.callback(now.strftime("%H:%M:%S"))
        self.now = now
