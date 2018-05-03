# -*- coding: utf-8 -*-

"""Main module."""
import attr
from serial import Serial

from flipapps.flipapps import FlipApps
from flipapps.app import ImageDetails
from pyflipdot.pyflipdot import HanoverController, HanoverSign


_DEAD_TIME_S = 2


def _test_draw(image: np.array):
    test_image = np.full(image.shape, ' ')
    test_image[image] = '#'
    for row in test_image:
        print("|{}|".format(''.join(list(row))))

@attr.s(frozen=True)
class SignParams(object):
    address = attr.ib(type=int)
    size = attr.ib(type=ImageDetails)
    flip = attr.ib(type=bool)


_SIGNS = {
    'upper': SignParams(1, ImageDetails(84, 7), True),
    'lower': SignParams(2, ImageDetails(84, 7), False),
}

class Runner(object):
    def run(self, port_name: str):
        # Create a controller
        port = Serial(port_name)
        self.controller = HanoverController(port)

        # Add signs and determine total image size
        image_size = ImageDetails(0, 0)
        for name, params in _SIGNS:
            # Create drivers for each sign and add to controller
            sign = HanoverSign(
                name, params.address,
                params.size.width, params.size.height,
                params.flip)
            controller.add_sign(sign)
            # Build dimensions of a stacked 'image'
            if image_size.width == 0:
                image_size.width = params.size.width
            assert image_size.width == params.size.width
            image_size.height += params.size.height

        # Create flipapps, passing image of combined signs
        apps = FlipApps(image_size, self._draw_image)
        apps.run()

    async def _draw_image(self, image: np.array):
        # Ensure we are able to draw
        dead_time_remaining = _DEAD_TIME_S - (time.time() - self.last_draw_time)
        if dead_time_remaining > 0:
            await asyncio.sleep(dead_time_remaining)

        row = 0
        for sign_name, sign in _SIGNS:
            # Get next horizontal slice of image
            sub_image = image[row:row+sign.height]
            # Draw the image to the corresponding sign
            self.controller.draw_image(sub_image, sign_name)
            # Update the current row
            row += sign.height
        self.last_draw_time = time.time()


@click.command()
@click.option(
    '--port',
    prompt="The serial port",
    help="The name of the serial port connected to the sign")
def main(port, sign):
    runner = Runner()
    runner.run(port)
