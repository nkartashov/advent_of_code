from typing import (
    List,
    NamedTuple,
    Tuple,
    Dict,
    Union,
    Deque,
    Set,
    Optional,
    Iterable,
    FrozenSet,
)
from enum import Enum
from collections import deque
from itertools import product, combinations, chain
import traceback
import tqdm
import time
import math

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")


TEST_DATA = """1
2
-3
3
-2
0
4""".split(
    "\n"
)


def parse(lines: List[str]) -> List[int]:
    return [int(line) for line in lines]


def mix(values: List[int]) -> List[int]:
    result = deepcopy(values)
    for value in values:
        idx = result.index(value)
        new_idx = -1
        if value > 0:
            new_idx = (idx + value) % len(values) + (idx + value) // len(values)
        else:
            if (idx + value) != 0 and (idx + value) % len(values) == 0:
                new_idx = len(values) - 1
            else:
                new_idx = (idx + value) % len(values)

        if new_idx < idx:
            result = (
                result[:new_idx] + [value] + result[new_idx:idx] + result[idx + 1 :]
            )
        else:
            result = (
                result[:idx]
                + result[idx + 1 : new_idx + 1]
                + [value]
                + result[new_idx + 1 :]
            )

        print(result)

    return values


def solve1(lines: List[str]) -> int:
    values = parse(lines)
    values = mix(values)

    return sum(values[idx % len(values)] for idx in [1000, 2000, 3000])


assrt(3, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    pass


assrt(301, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        # print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
