from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from collections import namedtuple

FONT_DIRECTORY = os.path.join(
    os.path.dirname(__file__),
    './hanover_flipdot/fonts')
TrueTypeFont = namedtuple('TrueTypeFont', ['path', 'points'])


def _font_path(path):
    return os.path.join(FONT_DIRECTORY, path)


FONTS = {
    'silkscreen': TrueTypeFont(
        _font_path('silkscreen/slkscr.ttf'), 6),
    'silkscreen bold': TrueTypeFont(
        _font_path('silkscreen/slkscrb.ttf'), 6),
    'silkscreen wide': TrueTypeFont(
        _font_path('silkscreen/slkscre.ttf'), 6),
    'Silkscreen wide bold': TrueTypeFont(
        _font_path('silkscreen/slkscreb.ttf'), 6),
    'high pixel font': TrueTypeFont(
        _font_path('7x4-High-Pixel-Font/7x4 High Pixel Font.ttf'), 2),
    'edge': TrueTypeFont(
        _font_path('Edge-7x7/Edge 7x7.ttf'), 6),
    'nintendo': TrueTypeFont(
        _font_path('Nintendo-Entertainment-System/Nintendo Entertainment System.ttf'), 6),
    'old school games': TrueTypeFont(
        _font_path('Old-School-Games/Old-School Games.ttf'), 6),
    'monopixel': TrueTypeFont(
        _font_path('7x7-Monopixel/7x7 Monopixel.ttf'), 6),
}


class TextBuilder(object):

    """Helper class for converting text to images

    Attributes:
        height (int): Height of the image
        width (int): Width of the image
    """

    def __init__(self, width: int, height: int):
        """Constructor for a TextHelper object

        Args:
            width (int): Width of the output text images
            height (int): Height of the output text images
        """
        self.width = width
        self.height = height

    def text_image(
            self,
            text: str,
            font: ImageFont,
            alignment='left'):
        """Creates an image from text

        Args:
            text (str): Text to convert to an image
            font (ImageFont): Font to use to render the image
            alignment (str, optional): Alignment ('left', 'right' or 'centre')

        Returns:
            TYPE: Image data
        """

        # Get some details about the font
        size, (_, offset_y) = font.font.getsize(text)

        # Determine Text starting position
        text_position = self.get_text_position(size, alignment)
        text_position['y'] -= offset_y

        # Create a new image
        image = Image.new(mode='1', size=(self.width, self.height), color=0)
        # Get a drawing context
        draw = ImageDraw.Draw(image)

        # Draw text
        draw.text(
            (text_position['x'], text_position['y']),
            text,
            fill=1,
            font=font)
        return np.array(image)

    def get_text_position(self, size: int, alignment: str):
        """Determines the top-left position for the text sub-image

        Args:
            size (int): Size
            alignment (str): Text alignment ('left', 'right' or 'centre')

        Returns:
            dict: (x, y) position

        Raises:
            ValueError: Invalid alignment argument
        """
        width, height = size

        if (width > self.width) or (height > self.height):
            print((
                "Warning: {}x{} text will be clipped "
                "to fit on {}x{} image").format(
                    width, height, self.width, self.height))

        text_position = {
            'y': 0
        }

        # Find x-position based on alignment
        if alignment == 'left':
            text_position['x'] = 0
        elif alignment == 'right':
            text_position['x'] = self.width - width
        elif alignment == 'centre':
            text_position['x'] = int(round((self.width - width) / 2))
        else:
            raise ValueError("Invalid alignment '{}'".format(alignment))

        return text_position
