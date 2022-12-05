from typing import List, NamedTuple, Tuple
from enum import Enum


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class Interval(NamedTuple):
    s: int
    e: int

    def contains(self, other: "Interval") -> bool:
        return self.s <= other.s and self.e >= other.e

    def overlap(self, other: "Interval") -> bool:
        if self.s > other.s:
            # xD
            self, other = other, self

        return not self.e < other.s


def parse_interval(inp: str) -> Interval:
    s, e = inp.split("-")
    return Interval(s=int(s), e=int(e))


def parse_line(line: str) -> List[Interval]:
    parts = line.split(",")
    assert len(parts) == 2
    return [parse_interval(part) for part in parts]


def solve1(lines: List[str]) -> int:
    result = 0
    for line in lines:
        intervals = parse_line(line)
        if intervals[0].contains(intervals[1]) or intervals[1].contains(intervals[0]):
            result += 1

    return result


TEST_DATA = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".split(
    "\n"
)

assrt(2, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    result = 0
    for line in lines:
        intervals = parse_line(line)
        if intervals[0].overlap(intervals[1]):
            result += 1

    return result


assrt(4, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
