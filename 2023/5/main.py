import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math
from typing import Optional


class Interval(BaseModel):
    start: int
    # Length inclusive.
    length: int

    def do_intersect(self, other: "Interval") -> bool:
        if other.start < self.start:
            self, other = other, self

        return not (self.start + self.length <= other.start)


aex(False, Interval(start=1, length=2).do_intersect(Interval(start=3, length=2)))
aex(True, Interval(start=1, length=2).do_intersect(Interval(start=2, length=2)))
aex(False, Interval(start=1, length=2).do_intersect(Interval(start=4, length=2)))


class MapInterval(BaseModel):
    src: Interval
    dst: Interval

    def apply(self, x: int) -> Optional[int]:
        if x < self.src.start or x >= self.src.start + self.src.length:
            return None

        return self.dst.start + x - self.src.start

    def apply_interval(
        self, i: Interval
    ) -> tuple[Optional[Interval], Optional[Interval]]:
        if not self.src.do_intersect(i):
            return None, i

        start = max(self.src.start, i.start)
        end = min(self.src.start + self.src.length, i.start + i.length)
        diff = self.dst.start - self.src.start
        assert end > start
        intersecton = Interval(start=start + diff, length=end - start)
        if intersecton.length == i.length:
            return intersecton, None

        if start == i.start:
            return intersecton, Interval(
                start=i.start + intersecton.length,
                length=i.length - intersecton.length,
            )

        return intersecton, Interval(
            start=i.start,
            length=i.length - intersecton.length,
        )


aex(
    (Interval(start=84, length=1), None),
    MapInterval(
        src=Interval(start=50, length=48), dst=Interval(start=52, length=48)
    ).apply_interval(Interval(start=82, length=1)),
)


def defrag(intervals: list[Interval]) -> list[Interval]:
    intervals.sort(key=lambda x: x.start)
    res = []
    i = 0
    while i < len(intervals):
        j = i + 1
        while j < len(intervals) and (
            intervals[i].do_intersect(intervals[j])
            or intervals[i].start + intervals[i].length == intervals[j].start
        ):
            j += 1

        end = intervals[j - 1].start + intervals[j - 1].length
        res.append(
            Interval(
                start=intervals[i].start,
                length=end - intervals[i].start,
            )
        )
        i = j

    return res


aex([Interval(start=1, length=2)], defrag([Interval(start=1, length=2)]))
aex(
    [Interval(start=1, length=3)],
    defrag([Interval(start=2, length=2), Interval(start=1, length=2)]),
)


class Map(BaseModel):
    tag: str
    intervals: list[MapInterval]


class Setup(BaseModel):
    seeds: list[int]
    maps: list[Map]


SEEDS = "seeds: "
MAP = " map:"


def parse_map(lines: list[str], i: int) -> tuple[Map, int]:
    assert lines[i] == ""
    i += 1
    assert MAP in lines[i]
    tag = lines[i][: -len(MAP)]
    i += 1
    intervals = []
    while i < len(lines) and lines[i] != "":
        dst_start, src_start, length = [int(x) for x in lines[i].split()]
        intervals.append(
            MapInterval(
                dst=Interval(start=dst_start, length=length),
                src=Interval(start=src_start, length=length),
            )
        )
        i += 1
    return Map(tag=tag, intervals=intervals), i


def parse_setup(lines: list[str]) -> Setup:
    i = 0
    assert SEEDS in lines[i]
    seeds = [int(x) for x in lines[i][len(SEEDS) :].split()]
    i += 1
    maps = []

    while i < len(lines):
        m, i = parse_map(lines, i)
        maps.append(m)
    return Setup(seeds=seeds, maps=maps)


def solve1(lines: list[str]) -> int:
    setup = parse_setup(lines)
    seeds = setup.seeds
    for m in setup.maps:
        new_seeds = []
        for seed in seeds:
            new_seed = None
            for interval in m.intervals:
                if new_seed is None:
                    new_seed = interval.apply(seed)
            if new_seed is None:
                new_seed = seed
            new_seeds.append(new_seed)
        seeds = new_seeds

    return min(seeds)


TEST_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

aex(35, solve1(splitlines(TEST_INPUT)))


def solve2(lines: list[str]) -> int:
    setup = parse_setup(lines)
    intervals = []
    for i in range(0, len(setup.seeds), 2):
        intervals.append(Interval(start=setup.seeds[i], length=setup.seeds[i + 1]))

    for m in setup.maps:
        new_intervals = []
        for interval in intervals:
            for map_interval in m.intervals:
                new_interval, interval = map_interval.apply_interval(interval)
                if new_interval is not None:
                    new_intervals.append(new_interval)

                if interval is None:
                    break

            if interval is not None:
                # Interval is unmapped after all mappings.
                new_intervals.append(interval)

        intervals = defrag(new_intervals)

    return intervals[0].start


aex(46, solve2(splitlines(TEST_INPUT)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))


if __name__ == "__main__":
    main()
