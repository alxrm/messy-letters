import numpy as np

from PIL import Image

from prepare import extract_letter_rows, transform_to_array, extract_letters_from_row


def read_picture(file_path):
    return Image.open(file_path)


def read_picture_as_grayscale(file_path):
    return transform_to_grayscale(read_picture(file_path))


def read_as_array(file_path):
    image = read_picture(file_path)
    image = transform_to_grayscale(image)

    return transform_to_array(image)


def transform_to_grayscale(picture):
    return picture.convert("L")


img = read_picture('./res/table.jpg')
img = transform_to_grayscale(img)

row_pics = extract_letter_rows(img)
row = row_pics[-1]

row.show()

letters = extract_letters_from_row(row)

print(len(letters))

for lt in letters:
    lt.show()
