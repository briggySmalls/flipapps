from flipapps.app import App
from flipapps.text_builder import TextBuilder
import asyncio


class Writer(App):
    def _setup(self):
        self.text_builder = TextBuilder(*self.image_details)

    async def run(self, text, font):
        # Convert the text to a series of images
        images = self.text_builder.text_image(text, font_name=font)

        # Display the images
        for _, image in enumerate(images):
            text = self.draw_image(image)
            await asyncio.sleep(1)

        # Ensure the text is left for a bit
        await asyncio.sleep(10)
