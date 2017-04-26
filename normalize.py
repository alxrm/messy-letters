import numpy as np

from utils.images import pad_to_size
from utils.misc import shift_round, insert_list_at_index


class Normalizer:
    def __init__(self,
                 letter_sequence: list,
                 approx_row_size: int = 40,
                 whiteness_limit: int = 250,
                 whiteness_trim_width_scale: float = 0.8,
                 height_bias: float = 1.5,
                 width_rounding_offset: float = 0.7,
                 height_rounding_offset: float = 0.5,
                 min_scale_width: float = 0.7,
                 min_scale_height: float = 0.3):
        self._raw_sequence = letter_sequence
        self._approx_row_size = approx_row_size
        self._width_rounding_offset = width_rounding_offset
        self._height_rounding_offset = height_rounding_offset
        self._whiteness_limit = whiteness_limit
        self._whiteness_trim_width_scale = whiteness_trim_width_scale
        self._height_bias = height_bias
        self._min_scale_height = min_scale_height
        self._min_scale_width = min_scale_width
        self._means = self._letter_means()

        self.mean_w = self._means[0]
        self.mean_h = self._means[1]

    def _letter_means(self):
        widths = []
        heights = []

        for i, lt in enumerate(self._raw_sequence):
            widths.append(lt.width)
            heights.append(lt.height)

        return np.mean(widths), np.mean(heights) * self._height_bias

    def _approx_letter_matrix(self, letter_sequence):
        line = []
        all_lines = []

        for i, lt in enumerate(letter_sequence):
            line.append(lt)

            if (i + 1) % self._approx_row_size == 0 or i == len(letter_sequence) - 1:
                all_lines.append(line)
                line = []

        return all_lines

    def _split_into_rows(self, wrong_letter_img):
        rows_count = shift_round(wrong_letter_img.height / self.mean_h, self._height_rounding_offset)

        if rows_count == 0:
            return [wrong_letter_img]

        row_h = wrong_letter_img.height / rows_count
        row_pics = []

        for r in range(0, rows_count):
            top = row_h * r
            bot = min(wrong_letter_img.height, row_h * (r + 1))
            result_row = wrong_letter_img.crop((0, top, wrong_letter_img.width, bot))

            row_pics.append(result_row)

        return row_pics

    def _split_into_columns(self, wrong_letter_img):
        cols_count = shift_round(wrong_letter_img.width / self.mean_w, self._width_rounding_offset)

        if cols_count == 0:
            return [wrong_letter_img]

        col_w = wrong_letter_img.width / cols_count
        column_pics = []

        for c in range(0, cols_count):
            left = col_w * c
            right = min(wrong_letter_img.width, col_w * (c + 1))
            result_letter = wrong_letter_img.crop((left, 0, right, wrong_letter_img.height))

            column_pics.append(result_letter)

        return column_pics

    def _filter_out_small_width(self, letter_sequence):
        result = []

        for lt in letter_sequence:
            if lt.width / self.mean_w > self._min_scale_width:
                result.append(lt)

        return result

    def _filter_out_small_height(self, letter_sequence):
        result = []

        for lt in letter_sequence:
            if (lt.height * self._height_bias) / self.mean_h > self._min_scale_height:
                result.append(lt)

        return result

    def _trim_whiteness(self, letter_row_image):
        row_arr = np.array(letter_row_image)
        trim_range = []

        for i in range(0, letter_row_image.width):
            avg = np.average(row_arr[:, i])

            if avg > self._whiteness_limit and len(trim_range) == 0:
                continue

            if avg < self._whiteness_limit and len(trim_range) == 0:
                trim_range.append(i)
                continue

            if avg > self._whiteness_limit and len(trim_range) == 1:
                trim_range.append(i)
                break

        if len(trim_range) == 0:
            return letter_row_image
        elif len(trim_range) == 1 and trim_range[0] >= letter_row_image.width * self._whiteness_trim_width_scale:
            return letter_row_image
        elif len(trim_range) == 1 and trim_range[0] < letter_row_image.width * self._whiteness_trim_width_scale:
            return letter_row_image.crop((trim_range[0], 0, letter_row_image.width, letter_row_image.height))

        left, right = trim_range[0], trim_range[1]

        return letter_row_image.crop((left, 0, right, letter_row_image.height))

    def _normalize_letters_by_width(self, lines):
        letter_mtx = [l for l in lines]

        for i, line in enumerate(lines):
            shift = 0
            mutated = line

            for j, letter in enumerate(line):
                shifted = j + shift

                if letter.width > self.mean_w:
                    trimmed = self._trim_whiteness(letter_row_image=letter)
                    letters = self._split_into_columns(trimmed)

                    if len(letters) > 1:
                        mutated = insert_list_at_index(mutated, letters, shifted, True)
                        shift += (len(letters) - 1)
                    elif len(letters) == 1:
                        mutated[shifted] = trimmed

            letter_mtx[i] = mutated

        return letter_mtx

    def _normalize_letters_by_height(self, lines):
        letter_mtx = [l for l in lines]

        for i, line in enumerate(lines):
            for j, letter in enumerate(line):
                if letter.height > self.mean_h:
                    rows = self._split_into_rows(letter)

                    if len(rows) > 1:
                        for r_id, letter_row in enumerate(rows):
                            line_index = i + r_id
                            exclude = r_id == 0

                            letter_mtx[line_index] = insert_list_at_index(lines[line_index], [letter_row], j,
                                                                          exclude)

        return letter_mtx

    def normalized_letter_sequence(self):
        filtered = self._filter_out_small_width(self._raw_sequence)
        filtered = self._filter_out_small_height(filtered)

        approx_mtx = self._approx_letter_matrix(filtered)
        approx_mtx = self._normalize_letters_by_height(approx_mtx)
        approx_mtx = self._normalize_letters_by_width(approx_mtx)

        result_sequence = np.reshape(approx_mtx, -1)
        result_sequence = [pad_to_size(letter) for letter in result_sequence]

        return result_sequence
