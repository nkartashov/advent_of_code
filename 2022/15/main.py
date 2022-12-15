from typing import List, NamedTuple, Tuple, Dict, Union, Deque
from enum import Enum
from collections import deque

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


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


def solve2(lines: List[str]) -> int:
    pass


assrt(93, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
