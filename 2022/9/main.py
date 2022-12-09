from typing import List, NamedTuple, Tuple, Dict
from enum import Enum

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__}({args}, {kwargs}) returned {got}, expected {want}")


DIRECTION_TO_DIFF = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


class Command(NamedTuple):
    direction: str
    length: int


def parse(lines: List[str]) -> List[Command]:
    result = []
    for line in lines:
        parts = line.split()
        assert len(parts) == 2
        result.append(Command(direction=parts[0], length=int(parts[1])))
    return result


D = {(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)}


def are_adjacent(head: Tuple[int, int], tail: Tuple[int, int]) -> bool:
    x1, y1 = head
    x2, y2 = tail

    return (x1 - x2, y1 - y2) in D


assrt(True, are_adjacent, (0, 0), (0, 0))
assrt(True, are_adjacent, (0, 1), (0, 0))
assrt(True, are_adjacent, (0, 0), (1, 0))
assrt(True, are_adjacent, (1, 1), (1, 0))
assrt(True, are_adjacent, (1, 1), (0, 0))
assrt(True, are_adjacent, (-1, 1), (0, 0))
assrt(True, are_adjacent, (-1, 1), (0, 2))
assrt(False, are_adjacent, (-2, 2), (0, 2))


def sign(a: int, b: int) -> int:
    if a == b:
        return 0

    return (a - b) // abs(a - b)


def follow(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    if are_adjacent(head, tail):
        return tail

    x1, y1 = head
    x2, y2 = tail
    tail = x2 + sign(x1, x2), y2 + sign(y1, y2)

    assert are_adjacent(head, tail)

    return tail


assrt((0, 1), follow, (0, 2), (0, 0))
assrt((-2, 2), follow, (-3, 2), (-1, 2))


def solve1(lines: List[str]) -> int:
    commands = parse(lines)

    positions = set()
    head = (0, 0)
    tail = (0, 0)

    for command in commands:
        for _ in range(command.length):
            diff = DIRECTION_TO_DIFF[command.direction]
            head = head[0] + diff[0], head[1] + diff[1]
            tail = follow(head, tail)
            positions.add(tail)

    return len(positions)


TEST_DATA = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split(
    "\n"
)

assrt(13, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    commands = parse(lines)

    positions = set()
    snake: List[Tuple[int, int]] = [(0, 0)] * 10

    for command in commands:
        for _ in range(command.length):
            diff = DIRECTION_TO_DIFF[command.direction]
            snake[0] = snake[0][0] + diff[0], snake[0][1] + diff[1]
            for i in range(1, len(snake)):
                snake[i] = follow(snake[i - 1], snake[i])
            positions.add(snake[-1])

    return len(positions)


assrt(1, solve2, TEST_DATA)

TEST_DATA1 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".split(
    "\n"
)

assrt(36, solve2, TEST_DATA1)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
