import math

import numpy as np


def shift_round(float_val, limit):
    lo = math.floor(float_val)
    hi = lo + 1
    diff = float_val - lo

    return lo if diff < limit else hi


def insert_list_at_index(to, which, index, with_exclude=False):
    return to[:index] + which + to[index + 1 if with_exclude is True else 0:]


def matrix_to_array(matrix):
        return np.squeeze(np.asarray(matrix))[0]
