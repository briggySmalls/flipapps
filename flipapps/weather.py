from darksky import forecast
import geocoder
import os
from PIL import Image
import numpy as np
import math
import asyncio

from flipapps.app import App

CURRENT_DIR = os.path.dirname(__file__)
DARKSKY_KEY = os.environ['DARKSKY_KEY']
DEFAULT_UNITS = 'uk2'
DEFAULT_EXCLUDES = ['daily']
HOURS_TO_DISPLAY = 6
HOURS_INC = 2
ICON_SIZE = (7, 7)

SUPPORTED_ICONS = {
    'clear-day': './images/sun.png',
    'clear-night': './images/sun.png',
    'rain': './images/rain.png',
    # 'snow': './images/.png',
    # 'sleet': './images/.png',
    'wind': './images/wind.png',
    # 'fog': './images/.png',
    'cloudy': './images/cloud.png',
    'partly-cloudy-day': './images/partly-cloudy.png',
    'partly-cloudy-night': './images/partly-cloudy.png',
}


def get_icon(icon):
    if icon not in SUPPORTED_ICONS:
        # TODO: Fallback to default icon?
        return None

    icon_path = os.path.join(CURRENT_DIR, SUPPORTED_ICONS[icon])
    print(icon_path)
    return np.asarray(Image.open(icon_path))


class Weather(App):
    def _setup(self):
        # Get location based off IP
        geo_helper = geocoder.ip('me')
        self.location = geo_helper.latlng

    async def run(self, *args, **kwargs):
        coordinates = kwargs['coordinates']
        # Default to using our current location
        if coordinates is None:
            coordinates = self.location

        # Request weather data from darksky
        forecast_data = forecast(
            DARKSKY_KEY,
            *coordinates,
            units=DEFAULT_UNITS,
            exclude=','.join(DEFAULT_EXCLUDES))

        # Create an image from the forecast
        print(forecast_data.hourly[0]['icon'])
        image = self._forecast_image(forecast_data)
        self.draw_image(image)

        # Ensure the results of the app are displayed for some time
        await asyncio.sleep(10)

    def _forecast_image(self, data, hour_count=None):
        image = self.create_image()
        (image_height, image_width) = image.shape
        (icon_height, icon_width) = ICON_SIZE
        assert image_height >= icon_height

        if hour_count is None:
            print(image_width)
            print(icon_width)
            # Determine how many hours we can fit on the image
            hour_count = math.floor(image_width / (icon_width + 2))

        # Determine location of icons
        icon_locs = np.linspace(0, image_width, hour_count + 2)

        # Draw icons along image
        for hour_idx in range(0, hour_count):
            # Get icon based off forecast
            hour_forecast = data.hourly[hour_idx]
            icon_array = get_icon(hour_forecast['icon'])

            # Add icon to image
            left = int(math.floor(icon_locs[hour_idx + 1] - icon_width / 2))
            image[0:icon_height, left:left + icon_width] = icon_array

        return image
