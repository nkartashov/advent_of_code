from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict

PREAMBLE_SIZE = 25

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def find_differences(adapters):
    # Difference of 3 to account for the last adapter
    result = [0, 0, 1]
    # Account for the first adapter in the chain.
    result[adapters[0] - 1] += 1
    for i, adapter in enumerate(adapters[1:], start=1):
        diff = adapter - adapters[i - 1]
        if diff:
            result[diff - 1] += 1
    return result


TEST_NUMBERS1 = list(sorted([int(line) for line in """16
10
15
5
1
11
7
19
6
12
4""".split()]))

TEST_NUMBERS2 = list(sorted([int(line) for line in """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".split()]))

ass([7, 0, 5], find_differences, TEST_NUMBERS1)
ass([22, 0, 10], find_differences, TEST_NUMBERS2)

def count_arrangements(adapters):
    cache = dict()
    def helper(prev, current_idx):
        key = prev, current_idx
        if key not in cache:
            current = adapters[current_idx]
            result = 0
            if current - prev <= 3:
                if current_idx == len(adapters) - 1:
                    result = 1
                else:
                    result += helper(current, current_idx + 1)
                    result += helper(prev, current_idx + 1)
            cache[key] = result
            
        return cache[key]

    # Result is running the algo when previous value is 0 (start) and all
    # adapters are available.
    return helper(0, 0)

ass(8, count_arrangements, TEST_NUMBERS1)
ass(19208, count_arrangements, TEST_NUMBERS2)

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        numbers = list(sorted(map(int, lines)))
        one_diff, _, three_diff = find_differences(numbers)
        print(one_diff * three_diff)
        print(count_arrangements(numbers))


if __name__ == "__main__":
    main()
