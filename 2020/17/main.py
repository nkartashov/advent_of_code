from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

ACTIVE = '#'

def transform_input_field_into_active_set(field, dimensions=3):
    result = set()
    for y, row in enumerate(field):
        for x, value in enumerate(row):
            if value == ACTIVE:
                result.add(tuple([x, y] + [0] * (dimensions - 2)))
    return result

D_COORD = [0, 1, -1]
D_CELL3 = list(product(D_COORD, D_COORD, D_COORD))[1:]
D_CELL4 = list(product(D_COORD, D_COORD, D_COORD, D_COORD))[1:]

@lru_cache(maxsize=10 ** 6)
def get_neighbours(cell):
    D_CELL = D_CELL4
    if len(cell) == 3:
        D_CELL = D_CELL3
    return [tuple(c + d_cell[i] for i, c in enumerate(cell)) for d_cell in D_CELL]

assrt(D_CELL3, get_neighbours, (0, 0, 0))
assrt(D_CELL4, get_neighbours, (0, 0, 0, 0))


# Expects a set of active coordinates
def simulate_cycle(active_set):
    updated_set = set()
    active_neighbour_count = defaultdict(int)
    for cell in active_set:
        for neighbour in get_neighbours(cell):
            active_neighbour_count[neighbour] += 1

    def is_alive(cell):
        count = active_neighbour_count[cell]
        if count == 3:
            return True
        return cell in active_set and count == 2

    return {cell for cell in active_neighbour_count if is_alive(cell)}

def simulate_cycles(active_set, count):
    for _ in range(count):
        active_set = simulate_cycle(active_set)
    return len(active_set)

TEST_FIELD = """.#.
..#
###
""".split()

assrt(112, simulate_cycles, transform_input_field_into_active_set(TEST_FIELD), 6)
assrt(848, simulate_cycles, transform_input_field_into_active_set(TEST_FIELD, dimensions=4), 6)


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        active_set = transform_input_field_into_active_set(lines)
        timer
        with timer('part1'):
            print(simulate_cycles(active_set, 6))
        active_set4 = transform_input_field_into_active_set(lines, dimensions=4)
        with timer('part2'):
            print(simulate_cycles(active_set4, 6))



if __name__ == "__main__":
    main()
