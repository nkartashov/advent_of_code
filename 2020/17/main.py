from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

ACTIVE = '#'
INACTIVE = '.'

def transform_input_field_into_active_set(field):
    result = set()
    for y, row in enumerate(field):
        for x, value in enumerate(row):
            if value == ACTIVE:
                result.add((x, y, 0))
    return result

D_COORD = [0, 1, -1]
D_CELL = list(product(D_COORD, D_COORD, D_COORD))[1:]

@lru_cache(maxsize=10 ** 6)
def get_neighbours(cell):
    x, y, z = cell
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in D_CELL]


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

ass(112, simulate_cycles, transform_input_field_into_active_set(TEST_FIELD), 6)


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        active_set = transform_input_field_into_active_set(lines)
        print(simulate_cycles(active_set, 6))



if __name__ == "__main__":
    main()
