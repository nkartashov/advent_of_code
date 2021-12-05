from enum import Enum
from typing import NamedTuple, List, Tuple
from collections import defaultdict


class Coord(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"{self.x},{self.y}"


class Vent(NamedTuple):
    start: Coord
    end: Coord

    def is_axis_aligned(self):
        return self.start.x == self.end.x or self.start.y == self.end.y

    def __repr__(self):
        return f"{self.start} -> {self.end}"


def read_coord(coord: str) -> Coord:
    return Coord(*[int(x) for x in coord.split(",")])


def read_vent(vent: str) -> Vent:
    start, end = vent.split(" -> ")
    return Vent(start=read_coord(start), end=read_coord(end))


def find_d(x0: int, x1: int) -> int:
    if x0 == x1:
        return 0
    if x0 > x1:
        return -1
    return 1


def count_intersections(vents: List[Vent], include_diagonal=False) -> int:
    points = defaultdict(int)
    for vent in vents:
        if vent.is_axis_aligned() or include_diagonal:
            dx = find_d(vent.start.x, vent.end.x)
            dy = find_d(vent.start.y, vent.end.y)
            x, y = vent.start.x, vent.start.y
            while x != vent.end.x or y != vent.end.y:
                points[(x, y)] += 1
                x += dx
                y += dy
            points[(vent.end.x, vent.end.y)] += 1

    return sum(1 for _, count in points.items() if count > 1)


def parse_lines(lines: List[str]) -> List[Vent]:
    return [read_vent(line) for line in lines]


TEST_LINES = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split(
    "\n"
)
assert count_intersections(parse_lines(TEST_LINES)) == 5
assert count_intersections(parse_lines(TEST_LINES), True) == 12


def read_input() -> List[Vent]:
    with open("in.txt") as infile:
        return parse_lines([line.strip() for line in infile.readlines()])


def main():
    print(count_intersections(read_input()))
    print(count_intersections(read_input(), True))


if __name__ == "__main__":
    main()
