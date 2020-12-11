from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

D_POSITION = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 1),
    (1, 1),
]

OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'

def lines_to_list(lines):
    return [list(line) for line in lines]

def count_occupied(grid, i, j):
    result = 0
    for dx, dy in D_POSITION:
        new_i = i + dx
        new_j = j + dy
        if 0 <= new_i < len(grid[0]) and \
           0 <= new_j < len(grid) and \
           grid[new_j][new_i] == OCCUPIED:
               result += 1
    return result

def swap_occupied_if_needed(value, occupied):
    if value == EMPTY and occupied == 0:
        return OCCUPIED, True

    if value == OCCUPIED and occupied >= 4:
        return EMPTY, True

    return value, False

def simulate_life(grid, count_occupied=count_occupied, swap_occupied_if_needed=swap_occupied_if_needed):
    buf = [[FLOOR] * len(grid[0]) for row in grid]

    has_changed = True
    while has_changed:
        has_changed = False

        for j, row in enumerate(grid):
            for i, value in enumerate(row):
                if value == FLOOR:
                    continue

                occupied = count_occupied(grid, i, j)
                buf[j][i], changed = swap_occupied_if_needed(value, occupied)
                has_changed = has_changed or changed

        buf, grid = grid, buf

    return sum(sum(1 for value in row if value == OCCUPIED) for row in grid)

TEST_LAYOUT = lines_to_list("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split())

ass(37, simulate_life, TEST_LAYOUT)




def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        grid = lines_to_list(lines)
        print(simulate_life(grid))


if __name__ == "__main__":
    main()
