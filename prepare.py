import numpy as np
from misc import last_index_match


def transform_to_array(picture):
    return np.array(picture)


def extract_letter_rows(picture):
    """Returns a bunch of cropped images"""

    picture_arr = np.array(picture)
    h, w = picture_arr.shape
    white_line_avg = 220

    anchor_row = last_index_match(picture_arr, lambda r: np.average(r) == 255.0)
    bounds = (0, anchor_row, w, h)

    picture = picture.crop(bounds)
    picture_arr = np.array(picture)

    row_ranges = []
    current_range = []
    visited_eh = False

    for i, row in enumerate(picture_arr):
        row = picture_arr[i]
        avg = np.average(row)

        if avg > white_line_avg and len(current_range) == 0:
            continue

        if avg < white_line_avg and len(current_range) == 0:
            current_range.append(i)
            continue

        if avg < white_line_avg and len(current_range) == 1 and visited_eh is False:
            continue

        if avg > white_line_avg and len(current_range) == 1:
            visited_eh = True
            continue

        if avg < white_line_avg and len(current_range) == 1 and visited_eh is True:
            current_range.append(i - 1)
            row_ranges.append(current_range)
            current_range = [i]
            visited_eh = False

    result_pictures = []

    for row_range in row_ranges:
        bounds = (0, row_range[0], w, row_range[1])

        result_pictures.append(picture.crop(bounds))

    return result_pictures


def extract_letters_from_row(row_image):
    rows = np.array(row_image)
    h, w = rows.shape
    white_line_avg = 250

    letters = []
    letter_ranges = []
    current_range = []

    for i in range(0, w):
        avg = np.average(rows[:, i])

        if avg > white_line_avg and len(current_range) == 0:
            continue

        if avg < white_line_avg and len(current_range) == 0:
            current_range.append(i)
            continue

        if avg > white_line_avg and len(current_range) == 1:
            current_range.append(i)
            letter_ranges.append(current_range)
            current_range = []

    for letter_range in letter_ranges:
        bounds = (letter_range[0], 0, letter_range[1], h)

        letters.append(row_image.crop(bounds))

    return letters

