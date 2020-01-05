from PIL import Image, ImageFont, ImageDraw


def add_soon_at_space(event_image):
    # add block at top

    # add "Soon at SPACE"
    font__1 = ImageFont.truetype('LexendDeca-Regular.ttf', 35)
    txt = Image.new('RGBA', (event_image.int_width_px,
                             event_image.int_height_px), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    draw.text((96, 22), 'Soon at TAMI', font=font__1,
              fill=(255, 255, 255, 255))
    event_image.image = Image.alpha_composite(event_image.image, txt)

    return event_image
