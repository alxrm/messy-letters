from io import BytesIO

from IPython.core.display import Image, display


def display_img(image, fmt='png', retina=True):
    bio = BytesIO()
    image.save(bio, format=fmt)
    display(Image(bio.getvalue(), format=fmt, retina=retina))
