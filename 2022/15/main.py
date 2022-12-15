from typing import List, NamedTuple, Tuple, Dict, Union, Deque, Set, Optional, Iterable
from enum import Enum
from collections import deque
from itertools import product, combinations

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Sensor(NamedTuple):
    x: int
    y: int

    beacon_x: int
    beacon_y: int

    @property
    def distance_to_beacon(self):
        return dist(self.x, self.y, self.beacon_x, self.beacon_y)


def parse_x(s: str) -> int:
    return int(s.split("=")[1])


assrt(-2, parse_x, "x=-2")


def parse_xy_expr(s: str) -> Tuple[int, int]:
    return tuple(parse_x(x) for x in s.split(", "))


assrt((-2, 15), parse_xy_expr, "x=-2, y=15")


def parse_sensor(line: str) -> Sensor:
    l, r = line.split(": closest")
    return Sensor(*parse_xy_expr(l.split("at ")[1]), *parse_xy_expr(r.split("at ")[1]))


assrt(
    Sensor(x=2, y=18, beacon_x=-2, beacon_y=15),
    parse_sensor,
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
)


def parse(lines: List[str]) -> List[Sensor]:
    result = []
    for line in lines:
        result.append(parse_sensor(line))

    return result


TEST_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".split(
    "\n"
)


def solve1(lines: List[str], row=2000000) -> int:
    sensors = parse(lines)
    # All positions are in the row of interest.
    positions = set()
    for sensor in sensors:
        x, y = sensor.x, sensor.y
        diff = sensor.distance_to_beacon - abs(row - y)
        if diff >= 0:
            positions.add(x)

            while diff:
                positions.add(x + diff)
                positions.add(x - diff)
                diff -= 1

        if sensor.beacon_y == row and sensor.beacon_x in positions:
            positions.remove(sensor.beacon_x)

    return len(positions)


assrt(26, solve1, TEST_DATA, 10)


class Interval(NamedTuple):
    s: int
    # End is not inclusive.
    e: int

    def point_inside(self, x: int) -> bool:
        return self.s <= x < self.e

    def intersection(self, other: "Interval") -> Optional["Interval"]:
        a = self
        b = other
        if a.s > b.s:
            a, b = b, a
        if a.e <= b.s:
            return None

        s = max(a.s, b.s)
        e = min(a.e, b.e)
        if s == e:
            # Disallow empty intervals.
            return None

        return Interval(s=s, e=e)

    def remainder_of_intersection(self, other: "Interval") -> List["Interval"]:
        # We assume that other intersects this one.
        if self.s == other.s and self.e == other.e:
            return []

        left = Interval(s=self.s, e=other.s)
        right = Interval(s=other.e, e=self.e)
        if other.s > self.s and other.e < self.e:
            return [left, right]

        if other.s == self.s:
            return [right]

        assert other.e == self.e
        return [left]

    @property
    def size(self) -> int:
        assert self.e > self.s
        return self.e - self.s

    def __repr__(self):
        return f"({self.s}, {self.e})"


aex(None, Interval(s=5, e=15).intersection(Interval(s=2, e=3)))
aex(None, Interval(s=2, e=3).intersection(Interval(s=5, e=15)))
aex(Interval(s=5, e=10), Interval(s=2, e=10).intersection(Interval(s=5, e=15)))


aex(
    [Interval(s=2, e=5)],
    Interval(s=2, e=10).remainder_of_intersection(Interval(s=5, e=10)),
)
aex(
    [Interval(s=5, e=10)],
    Interval(s=2, e=10).remainder_of_intersection(Interval(s=2, e=5)),
)
aex(
    [Interval(s=2, e=3), Interval(s=5, e=10)],
    Interval(s=2, e=10).remainder_of_intersection(Interval(s=3, e=5)),
)
aex([], Interval(s=2, e=10).remainder_of_intersection(Interval(s=2, e=10)))


class Region(NamedTuple):
    intervals: List[Interval]

    def intersection(self, other: "Region") -> Optional["Region"]:
        result_intervals = [
            l.intersection(r) for l, r in zip(self.intervals, other.intervals)
        ]
        if any(i is None for i in result_intervals):
            return None

        return Region(intervals=result_intervals)

    def remainder_of_intersection(self, other: "Region") -> List["Region"]:
        # We assume that other intersects this one.
        remainders: List[List[Interval]] = [
            s.remainder_of_intersection(o)
            for s, o in zip(self.intervals, other.intervals)
        ]

        result = []

        for rem_count in range(1, len(remainders) + 1):
            # Choose a number of coordinates which use remainders,
            # other coordinates come from other.
            for rem_idx_comb in combinations(range(len(remainders)), rem_count):
                for intervals in product(
                    *[
                        remainders[i] if i in rem_idx_comb else [interval]
                        for i, interval in enumerate(other.intervals)
                    ]
                ):
                    result.append(Region(intervals=list(intervals)))

        return result

    @property
    def size(self) -> int:
        result = 1
        for i in self.intervals:
            result *= i.size
        return result

    def within(self, other: "Region") -> bool:
        intersection = self.intersection(other)
        return intersection is not None and intersection.size == self.size

    def point_inside(self, xs: Iterable[int]) -> bool:
        return all(i.point_inside(x) for i, x in zip(self.intervals, xs))

    def __repr__(self):
        return "<" + ", ".join(f"{i}" for i in self.intervals) + ">"


LEFT = Interval(s=0, e=5)
RIGHT = Interval(s=5, e=7)
TOP = Interval(s=-2, e=6)
BOTTOM = Interval(s=6, e=11)

WHOLE_X = Interval(s=0, e=7)

TEST_WHOLE_REGION = Region(
    intervals=[
        WHOLE_X,
        Interval(s=-2, e=11),
    ]
)

aex(
    [
        Region(intervals=[LEFT, BOTTOM]),
        Region(intervals=[RIGHT, TOP]),
        Region(intervals=[LEFT, TOP]),
    ],
    TEST_WHOLE_REGION.remainder_of_intersection(Region(intervals=[RIGHT, BOTTOM])),
)

TOP_TO_MID = Interval(s=-2, e=4)
MID = Interval(s=4, e=7)
MID_TO_BOTTOM = Interval(s=7, e=11)
aex(
    [
        Region(intervals=[WHOLE_X, TOP_TO_MID]),
        Region(intervals=[WHOLE_X, MID_TO_BOTTOM]),
    ],
    TEST_WHOLE_REGION.remainder_of_intersection(Region(intervals=[WHOLE_X, MID])),
)


# ManhattanRegion is either a rectangle or a half-rectangle, the point shows which side of the rectangle is INCLUDED.
class ManhattanRegion:
    def __init__(self, region: Region):
        self._region = region
        self._point: Optional[Tuple[int, int]] = None

    def empty(self):
        return self._region.size == 0

    def point_inside(self, point: Iterable[int]) -> bool:
        return self._region.point_inside(point)

    # Intersects with the Manhattan circle (4 triangles).
    def intersect(self, x: int, y: int, radius: int) -> List["ManhattanRegion"]:
        other = Region(
            intervals=[
                Interval(s=x - radius, e=x + radius + 1),
                Interval(s=y - radius, e=y + radius + 1),
            ]
        )

        intersection = self._region.intersection(other)
        if intersection is None:
            return [self]

    # Returns the only point in the region which is not excluded
    def pop_only(self) -> Tuple[int, int]:
        assert False


# Max inclusive.
def solve2(lines: List[str], min_x=0, max_x=4000000, min_y=0, max_y=4000000) -> int:
    sensors = parse(lines)

    max_x += 1
    max_y += 1

    regions = [
        ManhattanRegion(
            Region(intervals=[Interval(s=min_x, e=max_x), Interval(s=min_y, e=max_y)])
        )
    ]

    for sensor in sensors:
        new_regions = []
        for region in regions:
            new_regions.extend(
                region.intersect(
                    x=sensor.x, y=sensor.y, radius=sensor.distance_to_beacon
                )
            )

        regions = new_regions

    assert len(regions) == 1

    x, y = regions[0].pop_only()
    return x * 4000000 + y


assrt(56000011, solve2, TEST_DATA, 0, 20, 0, 20)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
