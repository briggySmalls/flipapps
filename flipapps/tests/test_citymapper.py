import pytest
from flipapps.citymapper import Citymapper
from flipapps.app import ImageDetails

SIGN_SIZE = (84, 7)
BUCKINGHAM_PALACE = (51.501467, -0.141890)
HOUSES_OF_PARLIAMENT = (51.499954, -0.124684)


@pytest.fixture
def sign():
    return ImageDetails(*SIGN_SIZE)

@pytest.fixture
async def draw_image(image):



@pytest.fixture
def app(draw_image):
    return Citymapper(sign, draw_image)


def test_now(event_loop, app):
    event_loop.run_until_complete(
        app.run(
            start=BUCKINGHAM_PALACE,
            end=HOUSES_OF_PARLIAMENT))
