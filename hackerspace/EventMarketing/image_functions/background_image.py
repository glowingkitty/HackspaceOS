from PIL import Image
import requests
from io import BytesIO
from os import path


def resize(image, max_width, max_height):
    if image.width <= image.height:
        wpercent = (max_width/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((max_width, hsize), Image.ANTIALIAS)
    else:
        hpercent = (max_height/float(image.size[1]))
        wsize = int((float(image.size[0])*float(hpercent)))
        image = image.resize((wsize, max_height), Image.ANTIALIAS)

    return image


def add_background_image(event_image):
    # add event image
    if event_image.event.url_featured_photo:
        response = requests.get(event_image.event.url_featured_photo)
        img__result = Image.open(BytesIO(response.content)).convert('RGBA')
    elif event_image.event.image_featured_photo:
        img__result = Image.open(
            event_image.event.image_featured_photo).convert('RGBA')
    else:
        if path.exists('hackerspace/Website/static/images/logo.png'):
            # else take default image
            img__result = Image.open(
                'hackerspace/Website/static/images/header_banner.jpg').convert('RGBA')
        else:
            img__result = None

    if img__result:
        img__result = resize(
            img__result, event_image.int_width_px, event_image.int_height_px)

        # center image
        int__move_image_up = round(
            (img__result.height - event_image.int_height_px)/2)
        event_image.image.paste(
            img__result, (0, -int__move_image_up), img__result)

    return event_image
