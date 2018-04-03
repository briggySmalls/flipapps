from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from collections import namedtuple

FONT_DIRECTORY = os.path.join(
    os.path.dirname(__file__),
    './fonts')
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
            font_name: str,
            alignment='left'):
        """Creates an image from text

        Args:
            text (str): Text to convert to an image
            font_name (str): Font name to use to render the image
            alignment (str, optional): Alignment ('left', 'right' or 'centre')

        Returns:
            TYPE: Image data
        """

        # Get some details about the font
        font = self._get_font(font_name)
        lines = self._get_lines(text, font)

        images = []
        for line in lines:
            size, (_, offset_y) = font.font.getsize(line)

            # Determine Text starting position
            text_position = self._get_text_position(size, alignment)
            text_position['y'] -= offset_y

            # Create a new image
            image = Image.new(
                mode='1', size=(self.width, self.height), color=0)
            # Get a drawing context
            draw = ImageDraw.Draw(image)

            # Draw text
            draw.text(
                (text_position['x'], text_position['y']),
                line,
                fill=1,
                font=font)
            images.append(np.array(image))

        return images

    def _get_lines(self, text, font):
        # Assert that the font is appropriate
        (_, height), (_, _) = font.font.getsize(text)
        if height > self.height:
            raise RuntimeError("Font too tall for {}x{} image".format(
                self.width, self.height))

        # Convert the text into multiple lines
        lines = []
        while text:
            line, text = self._get_line(text, font, self.width)
            lines.append(line)
        return lines

    @staticmethod
    def _get_line(text, font, total_width):
        # First check if text fits on one line
        (width, _), (_, _) = font.font.getsize(text)
        if width <= total_width:
            # All the text fits on one line
            return text.strip(), ""

        def words_to_line(words):
            return ' '.join(words)

        all_words = text.split()
        previous_line = None
        for i, word in enumerate(all_words):
            # Create a new line with 'i' words
            query_line = words_to_line(all_words[:i])
            (width, _), _ = font.font.getsize(query_line)

            # Check if line is too long
            if width > total_width:
                if i == 0:
                    raise RuntimeError(
                        "'{}' is too long to fit in image".format(word))

                # We have found the word that makes the line too long
                text = text[len(previous_line):]
                text.strip()
                return previous_line, text

            # Iterate
            previous_line = query_line

    def _get_text_position(self, size, alignment: str):
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

        if width > self.width:
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

    @staticmethod
    def _get_font(font: str):
        # Get a font and its height
        font_details = FONTS[font]
        return ImageFont.truetype(
            font_details.path,
            int(font_details.points / 3 * 4))
