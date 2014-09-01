# Written by Timon Knigge, 2014
# Implements the Hungarian Algorithm.
# http://en.wikipedia.org/wiki/Hungarian_algorithm

import copy


def minimize(matrix):
    matrix = copy.deepcopy(matrix)

    for row in matrix:
        m = min(row)
        if m != 0:
            row[:] = map(lambda x: x - m, row)

    for i in range(len(matrix)):  # There is no other way!
        m = min(row[i] for row in matrix)
        if m != 0:
            for row in matrix:
                row[i] -= m
