from typing import List, NamedTuple, Set, Tuple, Optional
from enum import Enum
from collections import defaultdict, deque
from copy import deepcopy
from itertools import product
from functools import lru_cache
import math

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

SIZE = 10

D_COORD = [0, 1, -1]
D_CELL2 = list(product(D_COORD, D_COORD))[1:]

def get_neighbours(cell):
    return [tuple(c + d_cell[i] for i, c in enumerate(cell)) for d_cell in D_CELL2]

assrt(D_CELL2, get_neighbours, (0, 0))

def simulate_flashes(data: List[List[int]], steps=100, find_synchronisation=False) -> int:
    assert steps > 0 or find_synchronisation

    flash_count = 0
    current_step = 0
    while current_step < steps or find_synchronisation:
        has_flashed = set()
        current_step += 1
        new_data = [[value + 1 for value in row] for row in data]

        to_visit = [] 
        for i, row in enumerate(new_data):
            for j, value in enumerate(row):
                if value > 9:
                    to_visit.append((i, j))
                    has_flashed.add((i, j))

        while to_visit:
            i, j = to_visit.pop()
            for ni, nj in get_neighbours((i, j)):
                if 0 <= ni < SIZE and 0 <= nj < SIZE and (ni, nj) not in has_flashed:
                    new_data[ni][nj] += 1
                    if new_data[ni][nj] > 9:
                        to_visit.append((ni, nj))
                        has_flashed.add((ni, nj))

        for i, j in has_flashed:
            new_data[i][j] = 0
        data = new_data
        flash_count += len(has_flashed)
        if find_synchronisation and len(has_flashed) == SIZE * SIZE:
            return current_step
    return flash_count

def solve1(data, steps=100):
    return simulate_flashes(data, steps)

TEST_DATA = [[int(x) for x in row] for row in """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split()]
assrt(204, solve1, TEST_DATA, 10)

def solve2(data):
    return simulate_flashes(data, steps=-1, find_synchronisation=True)

assrt(195, solve2, TEST_DATA)

def main():
    with open('in.txt') as infile:
        data = [[int(x) for x in line.strip()] for line in infile.readlines()]
        assert len(data) == SIZE and len(data[0]) == SIZE
        print(solve1(data))
        print(solve2(data))


if __name__ == "__main__":
    main()
