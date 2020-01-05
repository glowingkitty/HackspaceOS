from PIL import Image
from os import path


def add_logo(event_image):
    # add logo to top left
    if path.exists('hackerspace/Website/static/images/logo.png'):
        img__logo = Image.open(
            'hackerspace/Website/static/images/logo.png').convert('RGBA')
        event_image.image.paste(img__logo, (10, 10), img__logo)

    return event_image
