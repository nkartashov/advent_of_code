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


def find_alignment_cost(locations: List[int]) -> int:
    result = sum(locations)
    location_counts = defaultdict(int)
    for location in locations:
        location_counts[location] += 1
    locations = list(sorted(location_counts.items()))
    left_count = 0
    right_count = sum(count for _, count in locations)
    prev_location = 0
    cost = result
    for location, count in locations:
        new_cost = cost + (left_count - right_count) * (location - prev_location)
        cost = new_cost
        result = min(result, cost)
        prev_location = location
        left_count += count
        right_count -= count

    return result

assrt(37, find_alignment_cost, [16,1,2,0,4,2,7,1,2,14])

def get_cost(x, y):
    diff = abs(x - y)
    return int(diff * (1 + diff) / 2)

assrt(66, get_cost, 5, 16)
assrt(66, get_cost, 16, 5)

def find_alignment_cost_linear_rate(locations: List[int]) -> int:
    min_location = min(locations)
    max_location = max(locations)
    result = get_cost(max_location, 0) * len(locations)
    location_counts = defaultdict(int)
    for location in locations:
        location_counts[location] += 1
    locations = list(sorted(location_counts.items()))
    for x in range(min_location, max_location + 1):
        cost = 0
        for location, count in locations:
            cost += get_cost(x, location) * count
        result = min(result, cost)

    return result

assrt(168, find_alignment_cost_linear_rate, [16,1,2,0,4,2,7,1,2,14])

def main():
    with open('in.txt') as infile:
        locations = [int(x) for x in infile.readline().strip().split(',')]
        print(find_alignment_cost(locations))
        print(find_alignment_cost_linear_rate(locations))


if __name__ == "__main__":
    main()
