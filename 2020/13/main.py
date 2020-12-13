from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

TEST_BUSES = '7,13,x,x,59,x,31,19'

def parse_busses(line):
    return [int(value) for value in line.split(',') if value != 'x']

ass([7, 13, 59, 31, 19], parse_busses, TEST_BUSES)

def solve(depart_ts, buses):
    wait_time, bus = min((bus - depart_ts % bus, bus) for bus in buses)
    return wait_time * bus

ass(295, solve, 939, [7, 13, 59, 31, 19])

def main():
    with open('in.txt') as infile:
        depart_ts = int(infile.readline().strip())
        buses = parse_busses(infile.readline().strip())
        print(solve(depart_ts, buses))


if __name__ == "__main__":
    main()
