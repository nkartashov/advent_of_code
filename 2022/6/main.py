from typing import List, NamedTuple, Tuple
from enum import Enum

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def detect_unique_chars(line: str, count: int) -> int:
    chars = dict()
    for i, x in enumerate(line):
        if i > count - 1:
            to_delete = line[i - count]
            chars[to_delete] -= 1
            if chars[to_delete] == 0:
                del chars[to_delete]

        chars[x] = chars.get(x, 0) + 1
        if len(chars) == count:
            return i + 1

    assert (
        False
    ), f"Could not find a starting position with {count} unique characters in a row"


def solve1(line: str) -> int:
    return detect_unique_chars(line, 4)


TEST_LINE1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
TEST_LINE2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
TEST_LINE3 = "nppdvjthqldpwncqszvftbrmjlhg"
TEST_LINE4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
TEST_LINE5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"

assrt(7, solve1, TEST_LINE1)
assrt(5, solve1, TEST_LINE2)
assrt(6, solve1, TEST_LINE3)
assrt(10, solve1, TEST_LINE4)
assrt(11, solve1, TEST_LINE5)


def solve2(line: str) -> int:
    return detect_unique_chars(line, 14)


assrt(19, solve2, TEST_LINE1)
assrt(23, solve2, TEST_LINE2)
assrt(23, solve2, TEST_LINE3)
assrt(29, solve2, TEST_LINE4)
assrt(26, solve2, TEST_LINE5)


def main():
    with open("in.txt") as infile:
        line = [line.strip() for line in infile.readlines()][0]
        print(solve1(line))
        print(solve2(line))


if __name__ == "__main__":
    main()
