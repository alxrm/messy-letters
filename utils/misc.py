import math

import numpy as np


def shift_round(float_val, limit):
    lo = math.floor(float_val)
    hi = lo + 1
    diff = float_val - lo

    return lo if diff < limit else hi


def insert_list_at_index(to, which, index, with_exclude=False):
    return to[:index] + which + to[index + 1 if with_exclude is True else 0:]


def flat_matrix(mtx):
    res = []

    for r in mtx:
        res += r

    return res


def partition_by_sizes(sequence, sub_sequence_sizes, default_size=40):
    default_size = default_size if sub_sequence_sizes is None else np.mean(sub_sequence_sizes)
    line = []
    all_lines = []
    line_counter = 0

    for index, element in enumerate(sequence):
        line.append(element)
        row_size = sub_sequence_sizes[line_counter] if line_counter < len(sub_sequence_sizes) else default_size

        if len(line) == row_size or index == len(sequence) - 1:
            all_lines.append(line)
            line = []
            line_counter += 1

    return all_lines
