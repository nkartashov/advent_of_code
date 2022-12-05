from typing import List, NamedTuple, Tuple
from enum import Enum

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


# Starting stacks
#             [M] [S] [S]
#         [M] [N] [L] [T] [Q]
# [G]     [P] [C] [F] [G] [T]
# [B]     [J] [D] [P] [V] [F] [F]
# [D]     [D] [G] [C] [Z] [H] [B] [G]
# [C] [G] [Q] [L] [N] [D] [M] [D] [Q]
# [P] [V] [S] [S] [B] [B] [Z] [M] [C]
# [R] [H] [N] [P] [J] [Q] [B] [C] [F]
#  1   2   3   4   5   6   7   8   9

STARTING_STACKS = [
    ["R", "P", "C", "D", "B", "G"],
    ["H", "V", "G"],
    ["N", "S", "Q", "D", "J", "P", "M"],
    ["P", "S", "L", "G", "D", "C", "N", "M"],
    ["J", "B", "N", "C", "P", "F", "L", "S"],
    ["Q", "B", "D", "Z", "V", "G", "T", "S"],
    ["B", "Z", "M", "H", "F", "T", "Q"],
    ["C", "M", "D", "B", "F"],
    ["F", "C", "Q", "G"],
]


class Command(NamedTuple):
    count: int
    f: int
    t: int


def parse_command(line: str) -> Command:
    parts = line.split()
    assert len(parts) == 6
    return Command(count=int(parts[1]), f=int(parts[3]) - 1, t=int(parts[5]) - 1)


def produce_result(stacks: List[List[str]]) -> str:
    return "".join(stack[-1] for stack in stacks if stack)


def solve1(lines: List[str], starting_stacks: List[List[str]] = STARTING_STACKS) -> str:
    stacks = deepcopy(starting_stacks)
    for line in lines:
        command = parse_command(line)
        boxes = stacks[command.f][-command.count :]
        stacks[command.f][-command.count :] = []
        stacks[command.t].extend(reversed(boxes))
    return produce_result(stacks)


TEST_STARTING_STACKS = [
    ["Z", "N"],
    ["M", "C", "D"],
    ["P"],
]

TEST_LINES = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".split(
    "\n"
)

assrt("CMZ", solve1, TEST_LINES, TEST_STARTING_STACKS)


def solve2(lines: List[str], starting_stacks: List[List[str]] = STARTING_STACKS) -> str:
    stacks = deepcopy(starting_stacks)
    for line in lines:
        command = parse_command(line)
        boxes = stacks[command.f][-command.count :]
        stacks[command.f][-command.count :] = []
        stacks[command.t].extend(boxes)
    return produce_result(stacks)


assrt("MCD", solve1, TEST_LINES, TEST_STARTING_STACKS)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
