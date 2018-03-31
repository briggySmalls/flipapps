# -*- coding: utf-8 -*-

"""Simple clock application"""
from datetime import datetime
from flipapps.app import App
from flipapps.text_builder import TextBuilder
from time import sleep


class Clock(App):
    def _setup(self):
        self.now = 0
        self.text_builder = TextBuilder(self.image_details.width, self.image_details.height)

    def _run(self, *args, **kwargs):
        while not self.is_cancel_requested:
            self._update_time()
            sleep(1)
        print("Clock dying...")

    def _update_time(self):
        # Get the current time
        now = datetime.now()
        if self.now == now:
            # We've drifted
            return

        # Create an image using the time, and draw it
        text = now.strftime("%H:%M:%S")
        images = self.text_builder.text_image(
            text, font_name='nintendo', alignment='centre')
        assert len(images) == 1
        self.draw_image(images[0])

        # Update record of previously sent time
        self.now = now
