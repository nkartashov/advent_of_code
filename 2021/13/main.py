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

class FoldType(Enum):
    VERTICAL = 'x'
    HORIZONTAL = 'y'

class Fold(NamedTuple):
    coord: int
    fold_type: FoldType

def read_input():
    dots = None
    folds = None
    with open('dots.txt') as infile:
        dots = [[int(x) for x in line.strip().split(',')] for line in infile.readlines()]
    with open('folds.txt') as infile:
        folds = []
        for line in infile.readlines():
            line = line.strip()
            _, _, value = line.split()
            axis, coord = value.split('=')
            folds.append(Fold(coord=int(coord), fold_type=FoldType(axis)))

    assert dots is not None
    assert folds is not None
    return dots, folds

def fold(dots, folds):
    maxx = max(x for x, y in dots)
    maxy = max(y for x, y in dots)
    data = [[False] * (maxx + 1) for _ in range(maxy + 1)]
    for x, y in dots:
        data[y][x] =  True

    for fold in folds:
        if fold.fold_type == FoldType.VERTICAL:
            x = fold.coord
            for j in range(x + 1, len(data[0])):
                newx = x - (j - x)
                for i in range(len(data)):
                    data[i][newx] = data[i][newx] or data[i][j]
            data = [row[:x] for row in data]

        if fold.fold_type == FoldType.HORIZONTAL:
            y = fold.coord
            for i in range(y + 1, len(data)):
                newy = y - (i - y)
                for j in range(len(data[0])):
                    data[newy][j] = data[newy][j] or data[i][j]
            data = data[:y]

    return data

def solve1(data):
    dots, folds = data
    new_data = fold(dots, folds[:1])
    return sum(sum(1 for x in row if x) for row in new_data)

TEST_DOTS = [
    (6,10),
    (0,14),
    (9,10),
    (0,3),
    (10,4),
    (4,11),
    (6,0),
    (6,12),
    (4,1),
    (0,13),
    (10,12),
    (3,4),
    (3,0),
    (8,4),
    (1,10),
    (2,14),
    (8,10),
    (9,0),
]
TEST_FOLDS = [
    Fold(coord=7, fold_type=FoldType.HORIZONTAL),
    Fold(coord=5, fold_type=FoldType.VERTICAL),
]

assrt(17, solve1, (TEST_DOTS, TEST_FOLDS))

def solve2(data):
    dots, folds = data
    new_data = fold(dots, folds)
    return '\n'.join(' '.join(('X' if x else ' ') for x in row) for row in new_data)

def main():
    data = read_input()
    print(solve1(data))
    print(solve2(data))


if __name__ == "__main__":
    main()
