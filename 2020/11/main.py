from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy

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

def make_swapper(max_occupied):
    def swap_occupied_if_needed(value, occupied):
        if value == EMPTY and occupied == 0:
            return OCCUPIED, True

        if value == OCCUPIED and occupied >= max_occupied:
            return EMPTY, True

        return value, False

    return swap_occupied_if_needed

def simulate_life(grid, count_occupied=count_occupied, swap_occupied_if_needed=make_swapper(4)):
    grid = deepcopy(grid)
    buf = deepcopy(grid)

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

def build_occupied_counter(grid):
    adjacent_seat_positions = defaultdict(list)

    def build_adjacent_seats_for_position(i, j):
        result = []
        for dx, dy in D_POSITION:
            new_i = i + dx
            new_j = j + dy
            while True:

                if new_i < 0 or new_i >= len(grid[0]) or \
                   new_j < 0 or new_j >= len(grid):
                    break

                if grid[new_j][new_i] != FLOOR:
                    result.append((new_i, new_j))
                    break

                new_i += dx
                new_j += dy
        return result

    for j, row in enumerate(grid):
        for i, value in enumerate(row):
            if value != FLOOR:
                adjacent_seat_positions[(i, j)] = build_adjacent_seats_for_position(i, j)

    def count_occupied(grid, i, j):
        return sum(1 for adj_i, adj_j in adjacent_seat_positions[(i, j)] if grid[adj_j][adj_i] == OCCUPIED)

    return count_occupied

def simulate_life_lines(grid):
    return simulate_life(grid, count_occupied=build_occupied_counter(grid), swap_occupied_if_needed=make_swapper(5))

ass(26, simulate_life_lines, TEST_LAYOUT)

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        grid = lines_to_list(lines)
        print(simulate_life(grid))
        print(simulate_life_lines(grid))


if __name__ == "__main__":
    main()
