import geocoder
import os
import numpy as np
import math
import asyncio
from datetime import datetime
import functools

import requests

from flipapps.app import App
from flipapps.text_builder import TextBuilder

CURRENT_DIR = os.path.dirname(__file__)
CITYMAPPER_KEY = os.environ['CITYMAPPER_KEY']
API_URI = "https://developer.citymapper.com/api/1/traveltime"


class Citymapper(App):
    def _setup(self):
        # Get location based off IP
        geo_helper = geocoder.ip('me')
        self.location = geo_helper.latlng
        self.text_builder = TextBuilder(
            self.image_details.width, self.image_details.height)

    async def run(self, end, start=None):
        # Default to using our current location
        if start is None:
            start = self.location

        # Request travel data from citymapper
        params = {
            'key': CITYMAPPER_KEY,
            'startcoord': start,
            'endcoord': end,
        }
        partial_func = functools.partial(
            requests.get,
            API_URI,
            params=params)
        response = await asyncio.get_event_loop().run_in_executor(
            None, partial_func)

        # Create an image from the forecast
        images = self.text_builder.text_image(
            response.json()['travel_time_minutes'], alignment='centre')
        assert len(images) == 1
        await self.draw_image(images[0])

        # Ensure the results of the app are displayed for some time
        await asyncio.sleep(10)
