from io import BytesIO

from PIL import Image as PImage
from IPython.core.display import Image, display


def display_img(image, fmt='png', retina=True):
    bio = BytesIO()
    image.save(bio, format=fmt)
    display(Image(bio.getvalue(), format=fmt, retina=retina))


def pad_to_size(src_image, w=64, h=64, pad_with_color=255):
    image_size = (w, h)

    # result image is always grayscale
    result_image = PImage.new('L', image_size, pad_with_color)

    left = int(result_image.width / 2 - src_image.width / 2)
    top = int(result_image.height / 2 - src_image.height / 2)
    right = left + src_image.width
    bottom = top + src_image.height

    paste_bounds = (left, top, right, bottom)

    result_image.paste(src_image, paste_bounds)

    return result_image
