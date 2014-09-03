# Written by Timon Knigge, 2014
# Implements the Hungarian Algorithm.
# http://en.wikipedia.org/wiki/Hungarian_algorithm

import copy
SIMPLE, STARRED, PRIMED = 0, 1, 2


def maximize(matrix):
    pass


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
            # Step 4(, 6)
            zero = _cover_zeroes(matrix, mask_matrix, row_cover, col_cover)

            # Step 5
            primes = [zero]
            stars = []
            while zero:
                zero = _find_star_in_col(mask_matrix, zero[1])
                if zero:
                    stars.append(zero)
                    zero = _find_prime_in_row(mask_matrix, zero[0])
                    stars.append(zero)

            for star in stars:
                mask_matrix[star[0]][star[1]] = SIMPLE

            for prime in primes:
                mask_matrix[prime[0]][prime[1]] = STARRED

            for r, row in enumerate(mask_matrix):
                for c, val in enumerate(row):
                    if val == PRIMED:
                        mask_matrix[r][c] = SIMPLE

            row_cover = [False] * n
            col_cover = [False] * n
            # end of step 5

        # end of step 3 while

    return mask_matrix


def _cover_zeroes(matrix, mask_matrix, row_cover, col_cover):

    # Repeat steps 4 and 6 until we are ready to break out to step 5
    while True:
        zero = True

        # Step 4
        while zero:
            zero = _find_noncovered_zero(matrix, row_cover, col_cover)
            if not zero:
                break  # continue with step 6
            else:
                row = mask_matrix[zero[0]]
                row[zero[1]] = PRIMED

                try:
                    index = row.index(STARRED)
                except ValueError:
                    return zero  # continue with step 5

                row_cover[zero[0]] = True
                col_cover[index] = False

        # Step 6
        m = min(_uncovered_values(matrix, row_cover, col_cover))
        for r, row in enumerate(matrix):
            for c, __ in enumerate(row):
                if row_cover[r]:
                    matrix[r][c] += m
                if not col_cover[c]:
                    matrix[r][c] -= m


def _find_noncovered_zero(matrix, row_cover, col_cover):
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0 and not row_cover[r] and not col_cover[c]:
                return (r, c)
    else:
        None


def _uncovered_values(matrix, row_cover, col_cover):
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if not row_cover[r] and not col_cover[c]:
                yield value


def _find_star_in_col(mask_matrix, c):
    for r, row in enumerate(mask_matrix):
        if row[c] == STARRED:
            return (r, c)
    else:
        return None


def _find_prime_in_row(mask_matrix, r):
    for c, val in enumerate(mask_matrix[r]):
        if val == PRIMED:
            return (r, c)
    else:
        return None


print(minimize([[  7,  53, 183, 439, 863],
             [497, 383, 563,  79, 973],
             [287,  63, 343, 169, 583],
             [627, 343, 773, 959, 943],
             [767, 473, 103, 699, 303]]))