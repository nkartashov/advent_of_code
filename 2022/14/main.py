from typing import List, NamedTuple, Tuple, Dict, Union, Deque
from enum import Enum
from collections import deque

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class Point(NamedTuple):
    x: int
    y: int

    @property
    def t(self):
        return self.x, self.y


def sign(x: int, y: int) -> int:
    if x == y:
        return 0

    return (x - y) // abs(x - y)


assrt(0, sign, 3, 3)
assrt(-1, sign, -5, -1)


def diff(start: Point, end: Point) -> Tuple[int, int]:
    return sign(end.x, start.x), sign(end.y, start.y)


assrt((0, -1), diff, Point(x=0, y=0), Point(x=0, y=-5))


class Map:
    def __init__(self, rocks: List[List[Point]]):
        min_x = 500
        max_x = 500
        max_y = 0
        for points in rocks:
            for point in points:
                min_x = min(min_x, point.x)
                max_x = max(max_x, point.x)
                max_y = max(max_y, point.y)

        self._max_x = max_x
        self._min_x = min_x
        self._max_y = max_y

        self._field = set()
        for points in rocks:
            for i in range(1, len(points)):
                start = points[i - 1]
                end = points[i]
                dx, dy = diff(start, end)
                self._field.add(end.t)
                x, y = start.t
                while (x, y) != end.t:
                    self._field.add((x, y))
                    x += dx
                    y += dy

    @property
    def size(self) -> int:
        return len(self._field)

    def has_item(self, x: int, y: int, floor_present=False) -> bool:
        return (x, y) in self._field or (floor_present and y == self._max_y + 2)

    def add_item(self, x: int, y: int):
        return self._field.add((x, y))

    def is_oob(self, x: int, y: int):
        return x < self._min_x or x > self._max_x or y > self._max_y


def parse(lines: List[str]) -> Map:
    rocks = []
    for line in lines:
        rocks.append(
            [Point(*map(int, point_str.split(","))) for point_str in line.split(" -> ")]
        )

    return Map(rocks=rocks)


TEST_DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".split(
    "\n"
)

assert parse(TEST_DATA).size == 20


def solve1(lines: List[str]) -> int:
    m = parse(lines)
    oob = False
    result = 0
    while not oob:
        x, y = 500, 0

        while True:
            if m.is_oob(x, y):
                oob = True
                break

            if not m.has_item(x, y + 1):
                y += 1
            elif not m.has_item(x - 1, y + 1):
                x -= 1
                y += 1
            elif not m.has_item(x + 1, y + 1):
                x += 1
                y += 1
            else:
                result += 1
                m.add_item(x, y)
                break

    return result


assrt(24, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    m = parse(lines)
    result = 0
    while not m.has_item(500, 0):
        x, y = 500, 0

        while True:
            if not m.has_item(x, y + 1, floor_present=True):
                y += 1
            elif not m.has_item(x - 1, y + 1, floor_present=True):
                x -= 1
                y += 1
            elif not m.has_item(x + 1, y + 1, floor_present=True):
                x += 1
                y += 1
            else:
                result += 1
                m.add_item(x, y)
                break

    return result


assrt(93, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
