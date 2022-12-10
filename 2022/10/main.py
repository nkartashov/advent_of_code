from typing import List, NamedTuple, Tuple, Dict, Union
from enum import Enum

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class NoOp:
    pass


class AddOp(NamedTuple):
    value: int


NOOP = "noop"


def parse(lines: List[str]) -> List[Union[NoOp, AddOp]]:
    result = []
    for line in lines:
        if line == NOOP:
            result.append(NoOp())
        else:
            result.append(AddOp(value=int(line.split()[1])))
    return result


D = """noop
addx 3
addx -5""".split(
    "\n"
)

CYCLES = {20, 60, 100, 140, 180, 220}


def solve1(lines: List[str]) -> int:
    result = 0
    instructions = parse(lines)
    x = 1
    cycle_counter = 1
    for instruction in instructions:
        if isinstance(instruction, NoOp):
            if cycle_counter in CYCLES:
                result += cycle_counter * x
            cycle_counter += 1

        elif isinstance(instruction, AddOp):
            if cycle_counter in CYCLES:
                result += cycle_counter * x
            cycle_counter += 1
            if cycle_counter in CYCLES:
                result += cycle_counter * x
            cycle_counter += 1
            x += instruction.value

    return result


TEST_DATA = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".split(
    "\n"
)

assrt(13140, solve1, TEST_DATA)


def update_result(screen: List[List[str]], cycle_counter: int, x: int):
    cycle_counter -= 1
    j = cycle_counter // 40
    i = cycle_counter % 40
    if cycle_counter % 40 in (x - 1, x, x + 1):
        screen[j][i] = "#"


def solve2(lines: List[str]) -> str:
    result = [["." for _ in range(40)] for _ in range(6)]
    instructions = parse(lines)
    x = 1
    cycle_counter = 1
    for instruction in instructions:

        if isinstance(instruction, NoOp):
            update_result(result, cycle_counter, x)
            cycle_counter += 1

        elif isinstance(instruction, AddOp):
            update_result(result, cycle_counter, x)
            cycle_counter += 1

            update_result(result, cycle_counter, x)
            cycle_counter += 1
            x += instruction.value

    return "\n".join("".join(row) for row in result)


TEST_RESULT = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

assrt(TEST_RESULT, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
