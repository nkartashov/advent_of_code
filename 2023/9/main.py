import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math
from typing import Optional
from collections import Counter
import re


def parse_input(lines: list[str]) -> list[list[int]]:
    return [[int(i) for i in line.split()] for line in lines]


def find_next_value(history: list[int], find_previous=False) -> int:
    i = 0
    levels = [history]
    while True:
        next_level = []
        levels.append(next_level)
        for j in range(1, len(levels[i])):
            next_level.append(levels[i][j] - levels[i][j - 1])

        if all(x == 0 for x in next_level):
            break
        i += 1

    if find_previous:
        for i in range(len(levels) - 2, -1, -1):
            levels[i].append(levels[i][0] - levels[i + 1][0])
            levels[i].reverse()
        return levels[0][0]

    for i in range(len(levels) - 2, -1, -1):
        levels[i].append(levels[i + 1][-1] + levels[i][-1])
    return levels[0][-1]


def solve1(lines: list[str]) -> int:
    histories = parse_input(lines)
    return sum(find_next_value(h) for h in histories)


TEST_INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

aex(114, solve1(splitlines(TEST_INPUT)))


def solve2(lines: list[str]) -> int:
    histories = parse_input(lines)
    return sum(find_next_value(h, find_previous=True) for h in histories)


aex(2, solve2(splitlines(TEST_INPUT)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))


if __name__ == "__main__":
    main()
