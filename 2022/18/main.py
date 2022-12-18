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

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")


TEST_DATA = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".split(
    "\n"
)


def parse_point(line: str) -> Tuple[int, int, int]:
    return tuple(int(x) for x in line.split(","))


def parse_points(lines: List[str]) -> Set[Tuple[int, int, int]]:
    result = set()
    for line in lines:
        result.add(parse_point(line))
    return result


D = [
    (0, 0, -1),
    (0, 0, 1),
    (0, -1, 0),
    (0, 1, 0),
    (-1, 0, 0),
    (1, 0, 0),
]

DD = list(product([0, -1, 1], repeat=3))[1:]


def solve1(lines: List[str]) -> int:
    points = parse_points(lines)
    result = 0
    for x, y, z in points:
        for dx, dy, dz in D:
            if (x + dx, y + dy, z + dz) not in points:
                result += 1

    return result


assrt(64, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    points = parse_points(lines)
    air_points = set()
    for x, y, z in points:
        for dx, dy, dz in DD:
            new_point = (x + dx, y + dy, z + dz)
            if new_point not in points:
                air_points.add(new_point)

    # Air points is all non-stone points which are adjacent to stone ones.
    start = air_points.pop()
    to_explore = deque([start])
    other_points = set([start])
    while to_explore:
        x, y, z = to_explore.pop()
        for dx, dy, dz in D:
            new_point = (x + dx, y + dy, z + dz)
            if new_point in air_points and new_point not in other_points:
                other_points.add(new_point)
                air_points.remove(new_point)
                to_explore.appendleft(new_point)

    # Now we have 2 sets: air_points and other_points.
    # One of them is inside, the other one - outside.
    to_visit = [deque(air_points), deque(other_points)]
    visited = [air_points, other_points]
    # Explore points in two sets until one of the sets is exhausted.
    # The exhausted set is inside.
    while all(to_visit):
        nodes = [q.pop() for q in to_visit]
        for i, (x, y, z) in enumerate(nodes):
            for dx, dy, dz in D:
                new_point = (x + dx, y + dy, z + dz)
                assert new_point not in visited[1 - i]
                # Not a stone point and not in the visited set.
                if new_point not in points and new_point not in visited[i]:
                    visited[i].add(new_point)
                    to_visit[i].appendleft(new_point)

    outside_points = visited[1] if not to_visit[0] else visited[0]
    result = 0
    for x, y, z in points:
        for dx, dy, dz in D:
            new_point = (x + dx, y + dy, z + dz)
            if new_point not in points and new_point in outside_points:
                result += 1

    return result


assrt(58, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
