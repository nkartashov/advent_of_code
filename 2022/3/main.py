from typing import List, NamedTuple
from enum import Enum


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def get_priority(item: str) -> int:
    assert len(item) == 1
    if "a" <= item <= "z":
        return ord(item) - ord("a") + 1

    return ord(item) - ord("A") + 27


assrt(1, get_priority, "a")
assrt(26, get_priority, "z")
assrt(27, get_priority, "A")
assrt(52, get_priority, "Z")


def solve1(lines: List[str]) -> int:
    result = 0
    for line in lines:
        assert len(line) % 2 == 0
        left = set(line[: len(line) // 2])
        right = set(line[len(line) // 2 :])
        item = (left & right).pop()
        result += get_priority(item)
    return result


TEST_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".split(
    "\n"
)

assrt(157, solve1, TEST_INPUT)


def solve2(lines: List[str]) -> int:
    result = 0
    assert len(lines) % 3 == 0
    for i in range(0, len(lines), 3):
        group = lines[i : i + 3]
        items = set(group[0])
        for elf in group:
            items = items & set(elf)
        assert len(items) == 1
        result += get_priority(items.pop())
    return result


assrt(70, solve2, TEST_INPUT)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
