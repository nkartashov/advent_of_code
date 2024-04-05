import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math
from typing import Optional
from collections import Counter, deque
import re


def find_start(field: list[str]) -> tuple[int, int]:
    for i, row in enumerate(field):
        for j, c in enumerate(row):
            if c == "S":
                return i, j
    raise ValueError("No start found")


D: list[tuple[tuple[int, int], str]] = [
    ((1, 0), "|LJ"),
    ((-1, 0), "|F7"),
    ((0, 1), "-7J"),
    ((0, -1), "-LF"),
]


def solve1(field: list[str]) -> int:
    start = find_start(field)
    dist = {start: 0}
    to_visit = deque([start])
    while to_visit:
        i, j = to_visit.popleft()
        for (di, dj), pipes in D:
            ii = i + di
            jj = j + dj

            if (
                ii < 0
                or ii >= len(field)
                or jj < 0
                or jj >= len(field[0])
                or (ii, jj) in dist
            ):
                continue

            if field[ii][jj] not in pipes:
                continue

            dist[(ii, jj)] = dist[(i, j)] + 1
            to_visit.append((ii, jj))

    return max(dist.values())


TEST_INPUT = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

aex(8, solve1(splitlines(TEST_INPUT)))


def solve2(lines: list[str]) -> int:
    histories = parse_input(lines)
    return sum(find_next_value(h, find_previous=True) for h in histories)


# aex(2, solve2(splitlines(TEST_INPUT)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    # print(solve2(lines))


if __name__ == "__main__":
    main()
