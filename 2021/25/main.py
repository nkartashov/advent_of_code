from re import S
from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any, FrozenSet
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import Error, deepcopy
from itertools import product, combinations
from functools import lru_cache
import math
from typing_extensions import ParamSpecArgs
from sortedcontainers import SortedDict
import functools
import operator
from tqdm import tqdm


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


TEST_INPUT = [
    list(line)
    for line in """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".split(
        "\n"
    )
]


def read_input():
    with open("in.txt") as infile:
        return [list(line.strip()) for line in infile.readlines()]


def p(f):
    print("\n".join("".join(row) for row in f))


def simulate(field: List[List[str]]) -> int:
    steps = 0
    moved = True
    while moved:
        moved = False
        steps += 1
        new_field = [[x for x in row] for row in field]
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == ">":
                    next_spot = j + 1 if j + 1 < len(field[i]) else 0
                    if field[i][next_spot] == ".":
                        moved = True
                        new_field[i][j] = "."
                        new_field[i][next_spot] = ">"
        field = new_field

        new_field = [[x for x in row] for row in field]
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == "v":
                    next_spot = i + 1 if i + 1 < len(field) else 0
                    if field[next_spot][j] == ".":
                        moved = True
                        new_field[i][j] = "."
                        new_field[next_spot][j] = "v"
        field = new_field

    return steps


assrt(58, simulate, TEST_INPUT)


def main():
    data = read_input()
    print(simulate(data))


if __name__ == "__main__":
    main()
