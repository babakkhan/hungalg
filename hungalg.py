# Written by Timon Knigge, 2014
# Implements the Hungarian Algorithm.
# http://en.wikipedia.org/wiki/Hungarian_algorithm

import copy
SIMPLE, STARRED, PRIMED = 0, 1, 2


def minimize(matrix):
    matrix = copy.deepcopy(matrix)
    n = len(matrix)

    # Step 1
    for row in matrix:
        m = min(row)
        if m != 0:
            row[:] = map(lambda x: x - m, row)

    mask_matrix = [[SIMPLE] * n for __ in matrix]
    row_cover = [False] * n
    col_cover = [False] * n

    # Step 2
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0 and not row_cover[r] and not col_cover[c]:
                mask_matrix[r][c] = STARRED
                row_cover[r] = True
                col_cover[c] = True

    row_cover = [False] * n
    col_cover = [False] * n

    # Step 3
    match_found = False

    while not match_found:
        for i in range(n):
            col_cover[i] = any(mrow[i] == STARRED for mrow in mask_matrix)

        if all(col_cover):
            match_found = True
            continue
        else:
            # Step 4
            _cover_zeroes(matrix, mask_matrix, row_cover, col_cover)
            # Step 5

def _cover_zeroes(matrix, mask_matrix, row_cover, col_cover):
    zero = True

    while zero:
        zero = _find_noncovered_zero(matrix, row_cover, col_cover)
        if zero:
            mask_matrix[zero[0]][zero[1]] = PRIMED

    # Step 6


def _find_noncovered_zero(matrix, row_cover, col_cover):
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0 and not row_cover[r] and not col_cover[c]:
                return (r, c)
    else:
        None