import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math
from typing import Optional


class Race(BaseModel):
    time: int
    distance: int


TIME = "Time:"
DISTANCE = "Distance:"


def parse_input(lines: list[str]) -> list[Race]:
    times = [int(t.strip()) for t in lines[0][len(TIME) :].split()]
    distances = [int(t.strip()) for t in lines[1][len(DISTANCE) :].split()]
    return [Race(time=t, distance=d) for t, d in zip(times, distances)]


def parse_input2(lines: list[str]) -> Race:
    time = int("".join([t.strip() for t in lines[0][len(TIME) :].split()]))
    distance = int("".join([t.strip() for t in lines[1][len(DISTANCE) :].split()]))
    return Race(time=time, distance=distance)


def get_ways_to_win(race: Race) -> int:
    # (total time - holding time) * holding time - distance
    D = (race.time**2 - 4 * race.distance) ** 0.5
    l = race.time / 2 - D / 2
    if math.ceil(l) > l:
        l = math.ceil(l)
    else:
        l = math.ceil(l) + 1

    r = race.time / 2 + D / 2
    if math.floor(r) < r:
        r = math.floor(r)
    else:
        r = math.floor(r) - 1
    return r - l + 1


aex(4, get_ways_to_win(Race(time=7, distance=9)))
aex(8, get_ways_to_win(Race(time=15, distance=40)))
aex(9, get_ways_to_win(Race(time=30, distance=200)))


def solve1(lines: list[str]) -> int:
    races = parse_input(lines)
    return math.prod(get_ways_to_win(r) for r in races)


TEST_INPUT = """Time:      7  15   30
Distance:  9  40  200"""

aex(288, solve1(splitlines(TEST_INPUT)))


def solve2(lines: list[str]) -> int:
    race = parse_input2(lines)
    return get_ways_to_win(race)


aex(71503, solve2(splitlines(TEST_INPUT)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))


if __name__ == "__main__":
    main()
