from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import Error, deepcopy, copy
from itertools import product
from functools import lru_cache
import math
from typing_extensions import ParamSpecArgs
from sortedcontainers import SortedDict
import functools
import operator


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


INPUT = 9, 4

MAX_POINTS = 1000
MAX_POSITION = 10
MAX_DIE = 100
ROLLS = 3


def solve1(positions):
    positions = [p - 1 for p in positions]
    scores = [0, 0]
    current_player = 1
    die = 0

    while scores[current_player] < MAX_POINTS:
        current_player = 1 - current_player
        for _ in range(ROLLS):
            positions[current_player] = (
                positions[current_player] + (die % MAX_DIE) + 1
            ) % MAX_POSITION
            die += 1
        scores[current_player] += positions[current_player] + 1

    return die * scores[1 - current_player]


TEST_INPUT = 4, 8
assrt(739785, solve1, TEST_INPUT)

MAX_DIRAC_POINTS = 21
MAX_DIRAC_DIE = 3

DIRAC_DIE_SIDES = [1, 2, 3]
DIRAC_OPTIONS = Counter(sum(l) for l in product(DIRAC_DIE_SIDES, repeat=3))


def solve2(positions):
    positions = [p - 1 for p in positions]
    cache = {}
    win_counts = defaultdict(int)

    def runner(positions, scores, current_player):
        key = tuple(positions), tuple(scores), current_player
        if key not in cache:
            result = [0, 0]
            if scores[current_player] >= MAX_DIRAC_POINTS:
                result[current_player] = 1
            else:
                current_player = 1 - current_player
                for die, mult in DIRAC_OPTIONS.items():
                    old_position = positions[current_player]
                    old_score = scores[current_player]

                    positions[current_player] = (
                        positions[current_player] + die
                    ) % MAX_POSITION
                    scores[current_player] += positions[current_player] + 1
                    subresult = runner(positions, scores, current_player)
                    for i, val in enumerate(subresult):
                        result[i] += val * mult

                    positions[current_player] = old_position
                    scores[current_player] = old_score
            cache[key] = result

        for i, val in enumerate(cache[key]):
            win_counts[i] += val
        return cache[key]

    scores = [0, 0]
    current_player = 1
    result = runner(positions, scores, current_player)
    return max(result)


assrt(444356092776315, solve2, TEST_INPUT)


def main():
    print(solve1(INPUT))
    print(solve2(INPUT))


if __name__ == "__main__":
    main()
