from PIL import Image, ImageFont, ImageDraw


from hackerspace.EventMarketing.image_functions.background_image import add_background_image
from hackerspace.EventMarketing.image_functions.add_logo import add_logo
from hackerspace.EventMarketing.image_functions.text import add_soon_at_space


class EventImage():
    def __init__(self, event):
        self.event = event
        self.layout = 1
        self.int_width_px = 500
        self.int_height_px = 500

        #########################

        self.image = Image.new(
            'RGBA', (self.int_width_px, self.int_height_px), (255, 255, 255, 0))
        self = add_background_image(self)
        self = add_logo(self)
        self = add_soon_at_space(self)

        # add background block
        # add event name
        # add event date and time
