from flipapps.app import App
from flipapps.text_builder import TextBuilder
from time import sleep


class Writer(App):
    def _setup(self):
        self.text_builder = TextBuilder(*self.image_details)

    def _run(self, text):
        images = self.text_builder.text_image(text, font_name='silkscreen')
        for _, image in enumerate(images):
            if self.is_cancel_requested:
                return

            text = self.draw_image(image)
            sleep(1)
