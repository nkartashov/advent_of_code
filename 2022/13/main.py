from typing import List, NamedTuple, Tuple, Dict, Union, Deque
from enum import Enum
from collections import deque
import functools

from copy import deepcopy

import traceback


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        print(f"{lineno}: {f.__qualname__} returned {got}, expected {want}")


def parse(text: str) -> List[List[list]]:
    return [
        [eval(line) for line in doubleline.split("\n")]
        for doubleline in text.split("\n\n")
    ]


TEST_DATA = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

assert parse(TEST_DATA)[0] == [[1, 1, 3, 1, 1], [1, 1, 5, 1, 1]]


class Result(Enum):
    GOOD = -1
    NEXT = 0
    BAD = 1


def compare(l, r) -> Result:
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return Result.GOOD

        if r < l:
            return Result.BAD

        return Result.NEXT

    if isinstance(l, list) and isinstance(r, list):
        i = 0
        j = 0

        while i < len(l) and j < len(r):
            result = compare(l[i], r[j])
            if result != Result.NEXT:
                return result

            i += 1
            j += 1

        if i != len(l):
            return Result.BAD

        if j != len(r):
            return Result.GOOD

        return Result.NEXT

    if not isinstance(l, list):
        l = [l]

    if not isinstance(r, list):
        r = [r]

    return compare(l, r)


assrt(Result.GOOD, compare, [1, 1, 3, 1, 1], [1, 1, 5, 1, 1])
assrt(Result.GOOD, compare, [[1], [2, 3, 4]], [[1], 4])
assrt(Result.BAD, compare, [9], [[8, 7, 6]])
assrt(Result.GOOD, compare, [[4, 4], 4, 4], [[4, 4], 4, 4, 4])
assrt(Result.BAD, compare, [7, 7, 7, 7], [7, 7, 7])
assrt(
    Result.BAD,
    compare,
    [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
    [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
)


def solve1(lines: str) -> int:
    pairs = parse(lines)
    result = 0
    for i, p in enumerate(pairs, start=1):
        comparison_result = compare(*p)
        assert comparison_result != Result.NEXT
        if comparison_result == Result.GOOD:
            result += i
    return result


assrt(13, solve1, TEST_DATA)


def solve2(lines: str) -> int:
    packets = [eval(line) for line in lines.split("\n") if line] + [[[2]], [[6]]]
    packets.sort(key=functools.cmp_to_key(lambda x, y: compare(x, y).value))
    i = packets.index([[2]]) + 1
    j = packets.index([[6]]) + 1
    return i * j


assrt(140, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = infile.read()
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
