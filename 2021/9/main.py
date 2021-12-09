from typing import List, NamedTuple, Set, Tuple
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

def get_neighbours(x: int, y: int):
    result = []
    D = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for dx, dy in D:
        newx = x + dx
        newy = y + dy
        result.append((x + dx, y + dy))
    return result

def find_low_points(data: List[List[int]]):
    result = []
    for x, row in enumerate(data):
        for y, value in enumerate(row):
            neighbours = [(nx, ny) for nx, ny in get_neighbours(x, y) if 0 <= nx < len(data) and 0 <= ny < len(data[nx])]
            if all(value < data[nx][ny] for nx, ny in neighbours):
                result.append((x, y))
    return result

def solve1(data: List[List[int]]):
    low_points = find_low_points(data)
    result = 0
    for x, y in low_points:
        result += data[x][y] + 1
    return result

def find_basin_size(start, data: List[List[int]]):
    result = 0
    points = deque([start])
    visited = {start}
    while points:
        result += 1
        x, y = points.popleft()
        visited.add((x, y))
        neighbours = [(nx, ny) for nx, ny in get_neighbours(x, y) if 0 <= nx < len(data) and 0 <= ny < len(data[nx])]
        for nx, ny in neighbours:
            if (nx, ny) not in visited and data[nx][ny] != 9 and data[x][y] < data[nx][ny]:
                visited.add((nx, ny))
                points.append((nx, ny))
    return result

TEST_DATA = [[int(x) for x in line.strip()] for line in """2199943210
3987894921
9856789892
8767896789
9899965678""".split()]

assrt(9, find_basin_size, (4, 6), TEST_DATA)

def solve2(data: List[List[int]]):
    low_points = find_low_points(data)
    top3 = list(sorted(find_basin_size(point, data) for point in low_points))[-3:]
    assert len(top3) == 3
    return math.prod(top3)



def main():
    with open('in.txt') as infile:
        data = [[int(x) for x in line.strip()] for line in infile.readlines()]
        print(solve1(data))
        print(solve2(data))


if __name__ == "__main__":
    main()
