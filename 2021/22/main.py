from re import S
from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import Error, deepcopy
from itertools import product, combinations
from functools import lru_cache
import math
from typing_extensions import ParamSpecArgs
from sortedcontainers import SortedDict
import functools
import operator
from tqdm import tqdm


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


class Interval(NamedTuple):
    s: int
    # End is not inclusive.
    e: int

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

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(s=min(self.s, other.s), e=max(self.e, other.e))

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

    def __add__(self, other: "Region") -> "Region":
        return Region(
            intervals=[a + b for a, b in zip(self.intervals, other.intervals)]
        )

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

    def size(self) -> int:
        result = 1
        for i in self.intervals:
            result *= i.size()
        return result

    def within(self, other: "Region") -> bool:
        intersection = self.intersection(other)
        return intersection is not None and intersection.size() == self.size()

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

START_INTERVAL = Interval(s=10, e=13)
START_CUBE = Region(intervals=[START_INTERVAL, START_INTERVAL, START_INTERVAL])

NEW_INTERVAL = Interval(s=11, e=14)
NEW_CUBE = Region(intervals=[NEW_INTERVAL, NEW_INTERVAL, NEW_INTERVAL])
INTERSECTION = NEW_CUBE.intersection(START_CUBE)
assert INTERSECTION is not None
aex(7, len(START_CUBE.remainder_of_intersection(INTERSECTION)))


class Step(NamedTuple):
    type: Type
    region: Region


def parse_interval(coords_text):
    s, e = [int(x) for x in coords_text.split("..")]
    # +1 to make non-inclusive.
    return Interval(s=s, e=e + 1)


def parse_line(line):
    type_text, rest = line.split(" ")
    intervals = [parse_interval(x.split("=")[1]) for x in rest.split(",")]
    return Step(type=Type(type_text), region=Region(intervals=intervals))


def parse_test_input(s: str) -> List[Step]:
    return [parse_line(line.strip()) for line in s.split("\n")]


TEST_STEPS1 = parse_test_input(
    """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""
)

TEST_STEPS2 = parse_test_input(
    """on x=-20..26,y=-36..17,z=-47..7
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
on x=967..23432,y=45373..81175,z=27513..53682"""
)

aex(
    Step(
        type=Type.ON,
        region=Region(
            [Interval(s=-20, e=27), Interval(s=-36, e=18), Interval(s=-47, e=8)]
        ),
    ),
    TEST_STEPS2[0],
)

aex(47 * 54 * 55, TEST_STEPS2[0].region.size())


def read_input():
    with open("in.txt") as infile:
        return [parse_line(line.strip()) for line in infile.readlines()]


INIT_LIMIT = Interval(s=-50, e=51)
INIT_REGION = Region(intervals=[INIT_LIMIT, INIT_LIMIT, INIT_LIMIT])


class SpaceTreeNode:
    def __init__(self, region: Region, type: Type):
        self._type = type
        self._region = region
        self._children: List[SpaceTreeNode] = []

    def is_terminal(self) -> bool:
        return len(self._children) == 0

    def process(self, region: Region, type: Type):
        assert region.within(self._region)

        if self.is_terminal():
            if self._type != type:
                if self._region == region:
                    self._type = type
                    return

                # Remember the subregion since we're not the same type.
                self._children.append(SpaceTreeNode(region=region, type=type))
            return

        # Pop the region into children. Since children don't intersect,
        # we can pop it into every child separately.
        regions = [region]
        for ch in self._children:
            new_regions = []
            for r in regions:
                if r.within(ch._region):
                    # Region is fully within child, no need to split.
                    ch.process(r, type)
                    continue

                intersection = r.intersection(ch._region)
                if intersection is not None:
                    # Process the intersecting part,
                    # get the remaining subregions for later processing.
                    ch.process(intersection, type)
                    new_regions.extend(r.remainder_of_intersection(intersection))
                else:
                    # No intersection, so save the subregion for later.
                    new_regions.append(r)

            regions = new_regions

        # Save all the remaining subregions.
        self._children.extend(SpaceTreeNode(region=r, type=type) for r in regions)

    def size(self) -> int:
        if self.is_terminal():
            return self._region.size() if self._type == Type.ON else 0

        if self._type == Type.ON:
            # The whole region is lit, so unlit regions can only be in children,
            # avoid double-counting by asking children for their lit size.
            result = self._region.size()
            for ch in self._children:
                result += -ch._region.size() + ch.size()
            return result

        # The whole region is unlit, so lit regions can only be in children,
        # ask children for sum of their lit parts.
        return sum(ch.size() for ch in self._children)

    def __repr__(self):
        return f"{self._region}: {self._type}"


def process_steps(steps: List[Step], check_initialization=True) -> int:
    region = INIT_REGION
    for step in steps:
        region = region + step.region

    tree = SpaceTreeNode(region=region, type=Type.OFF)
    for step in tqdm(steps):
        if not check_initialization or step.region.within(INIT_REGION):
            tree.process(step.region, step.type)

    return tree.size()


def solve1(steps: List[Step]) -> int:
    return process_steps(steps)


def solve2(steps: List[Step]) -> int:
    return process_steps(steps, check_initialization=False)


TEST_STEPS3 = parse_test_input(
    """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
)

assrt(39, solve1, TEST_STEPS1)
assrt(590784, solve1, TEST_STEPS2)
assrt(2758514936282235, solve2, TEST_STEPS3)


def main():
    data = read_input()
    res1 = solve1(data)
    assert res1 == 644257
    print(res1)
    res2 = solve2(data)
    assert res2 == 1235484513229032
    print(res2)


if __name__ == "__main__":
    main()
