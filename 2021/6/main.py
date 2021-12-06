from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def run_simulation(fishes: List[int], days=80) -> int:
    timers = [0] * 9
    for fish in fishes:
        timers[fish] += 1

    while days > 0:
        new_timers = [0] * 9
        for i, count in enumerate(timers):
            if i == 0:
                new_timers[6] += count
                new_timers[8] += count
            else:
                new_timers[i - 1] += count
        timers = new_timers

        days -= 1
    return sum(timers)

assrt(26, run_simulation, [3,4,3,1,2], 18)
assrt(5934, run_simulation, [3,4,3,1,2])
assrt(26984457539, run_simulation, [3,4,3,1,2], 256)

def main():
    with open('in.txt') as infile:
        fish = [int(x) for x in infile.readline().strip().split(',')]
        print(run_simulation(fish))
        print(run_simulation(fish, 256))


if __name__ == "__main__":
    main()
