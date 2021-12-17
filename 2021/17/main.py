from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import deepcopy
from itertools import product
from functools import lru_cache
import math
from sortedcontainers import SortedDict
import functools
import operator
import time


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def can_reach_target(dx, dy, minx, maxx, miny, maxy):
    x, y = 0, 0

    def can_still_reach():
        return not (y < miny or x > maxx) and not (x < minx and dx == 0)

    while can_still_reach():
        if minx <= x <= maxx and miny <= y <= maxy:
            return True

        x += dx
        y += dy
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1
        dy -= 1

    return False


# minx, maxx, miny, maxy
TARGET_AREA = [(139, 187), (-148, -89)]
MAX_Y_SPEED = 1000


def find_minimum_dx(minx, maxx) -> int:
    for dx in range(1, minx):
        # find maximum x distance that can be covered
        dist = dx * (dx + 1) // 2
        if minx <= dist <= maxx:
            return dx
    assert False


def solve_y(minx, maxx, miny, maxy) -> int:
    left = 1
    right = MAX_Y_SPEED
    dx = find_minimum_dx(minx, maxx)
    assert not can_reach_target(dx, right, minx, maxx, miny, maxy)
    mid = -1

    while right - left > 1:
        mid = left + (right - left) // 2
        if can_reach_target(dx, mid, minx, maxx, miny, maxy):
            left = mid
        else:
            right = mid

    assert mid > 0
    return mid * (mid + 1) // 2


assrt(45, solve_y, 20, 30, -10, -5)


def solve1() -> int:
    (minx, maxx), (miny, maxy) = TARGET_AREA
    return solve_y(minx, maxx, miny, maxy)


def find_candidate_dx_configurations(minx, maxx):
    result = []
    for dx in range(1, maxx + 1):
        x = 0
        idx = dx
        # Find all possible speeds where x reaches the target.
        while not ((x > maxx and dx >= 0) or (x < minx and dx == 0)):
            if minx <= x <= maxx:
                result.append(idx)
                break

            x += dx
            if dx > 0:
                dx -= 1
            elif dx < 0:
                dx += 1

    return result


def solve_all(minx, maxx, miny, maxy) -> int:
    candidate_dxs = find_candidate_dx_configurations(minx, maxx)
    result = 0
    for dx in candidate_dxs:
        for dy in range(miny, MAX_Y_SPEED):
            can_reach = can_reach_target(dx, dy, minx, maxx, miny, maxy)

            if can_reach:
                result += 1

    return result


assrt(112, solve_all, 20, 30, -10, -5)


def solve2() -> int:
    (minx, maxx), (miny, maxy) = TARGET_AREA
    return solve_all(minx, maxx, miny, maxy)


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
