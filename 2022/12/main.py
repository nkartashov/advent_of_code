from typing import List, NamedTuple, Tuple, Dict, Union, Deque
from enum import Enum
from collections import deque

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


Point = Tuple[int, int]


class Map(NamedTuple):
    data: List[List[str]]
    start: Point
    end: Point

    def height(self, i, j) -> int:
        value = self.data[j][i]

        if (i, j) == self.start:
            value = "a"

        if (i, j) == self.end:
            value = "z"

        return ord(value) - ord("a")


def parse(lines: List[str]) -> Map:
    result = []
    start = None
    end = None
    for j, line in enumerate(lines):
        result.append([x for x in line])
        for i, x in enumerate(line):
            if x == "S":
                start = (i, j)
            if x == "E":
                end = (i, j)

    assert start is not None
    assert end is not None

    return Map(data=result, start=start, end=end)


D = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def solve1(lines: List[str]) -> int:
    m = parse(lines)
    to_visit: Deque[Tuple[Point, int]] = deque([(m.end, 0)])
    visited = set([m.end])
    while to_visit:
        p, steps = to_visit.pop()
        if p == m.start:
            return steps

        for dx, dy in D:
            new_x = p[0] + dx
            new_y = p[1] + dy
            current = m.height(*p)
            new_p = (new_x, new_y)
            if (
                0 <= new_x < len(m.data[0])
                and 0 <= new_y < len(m.data)
                and new_p not in visited
                and current - m.height(*new_p) <= 1
            ):
                visited.add(new_p)
                to_visit.appendleft((new_p, steps + 1))

    assert False


TEST_DATA = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split(
    "\n"
)

assrt(31, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    m = parse(lines)
    to_visit: Deque[Tuple[Point, int]] = deque([(m.end, 0)])
    visited = set([m.end])
    while to_visit:
        p, steps = to_visit.pop()
        if p == m.start or m.height(*p) == 0:
            return steps

        for dx, dy in D:
            new_x = p[0] + dx
            new_y = p[1] + dy
            current = m.height(*p)
            new_p = (new_x, new_y)
            if (
                0 <= new_x < len(m.data[0])
                and 0 <= new_y < len(m.data)
                and new_p not in visited
                and current - m.height(*new_p) <= 1
            ):
                visited.add(new_p)
                to_visit.appendleft((new_p, steps + 1))

    assert False
    pass


assrt(29, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
