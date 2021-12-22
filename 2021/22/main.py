from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import Error, deepcopy
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


class Interval(NamedTuple):
    s: int
    e: int

    def intersection(self, other: "Interval") -> Optional["Interval"]:
        a = self
        b = other
        if a.s > b.s:
            a, b = b, a
        if a.e < b.s:
            return None

        s = max(a.s, b.s)
        e = min(a.e, b.e)
        if s == 0 or e == 0:
            # Disallow empty intervals.
            return None

        assert e > s
        return Interval(s=s, e=e)

    def size(self) -> int:
        assert self.e > self.s
        return self.e - self.s


aex(None, Interval(s=5, e=15).intersection(Interval(s=2, e=3)))
aex(None, Interval(s=2, e=3).intersection(Interval(s=5, e=15)))
aex(Interval(s=5, e=10), Interval(s=2, e=10).intersection(Interval(s=5, e=15)))


class Type(Enum):
    ON = "on"
    OFF = "off"


class Region(NamedTuple):
    intervals: List[Interval]

    def intersection(self, other: "Region") -> Optional["Region"]:
        result_intervals = [
            l.intersection(r) for l, r in zip(self.intervals, other.intervals)
        ]
        if any(i is None for i in result_intervals):
            return None
        return Region(intervals=result_intervals)

    def size(self) -> int:
        result = 1
        for i in self.intervals:
            result *= i.size()
        return result

    def within(self, other: "Region") -> bool:
        intersection = self.intersection(other)
        return intersection is not None and intersection.size() == self.size()


class Step(NamedTuple):
    type: Type
    region: Region


def parse_intervals(coords_text):
    return Interval(*[int(x) for x in coords_text.split("..")])


def parse_line(line):
    type_text, rest = line.split(" ")
    intervals = [parse_intervals(x.split("=")[1]) for x in rest.split(",")]
    return Step(type=Type(type_text), region=Region(intervals=intervals))


TEST_STEPS = [
    parse_line(line.strip())
    for line in """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".split(
        "\n"
    )
]

aex(
    Step(
        type=Type.ON,
        region=Region(
            [Interval(s=-20, e=26), Interval(s=-36, e=17), Interval(s=-47, e=7)]
        ),
    ),
    TEST_STEPS[0],
)


def read_input():
    with open("in.txt") as infile:
        return [parse_line(line.strip()) for line in infile.readlines()]


INIT_LIMIT = Interval(s=-50, e=50)
INIT_REGION = Region(intervals=[INIT_LIMIT, INIT_LIMIT, INIT_LIMIT])


def solve1(steps: List[Step]) -> int:
    cubes_on = set()

    for step in steps:
        if step.region.within(INIT_REGION):
            for cube in product(
                *[list(range(i.s, i.e + 1)) for i in step.region.intervals]
            ):
                if step.type == Type.ON:
                    cubes_on.add(cube)
                elif cube in cubes_on:
                    cubes_on.remove(cube)

    return len(cubes_on)


assrt(590784, solve1, TEST_STEPS)


def main():
    data = read_input()
    print(solve1(data))
    # print(solve2(*data))


if __name__ == "__main__":
    main()
