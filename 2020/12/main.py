from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class Direction(Enum):
    N = 'N'
    E = 'E'
    S = 'S'
    W = 'W'

    def cycle(self, shift):
        VALUES = [value for value in Direction]
        return VALUES[(VALUES.index(self) + shift) % len(VALUES)]

ass(Direction.N, Direction.S.cycle, 2)
ass(Direction.N, Direction.S.cycle, -6)

class Turn(Enum):
    L = 'L'
    R = 'R'

    def to_sign(self):
        if self is Turn.L:
            return -1
        return 1

class Move(Enum):
    F = 'F'

class Inst(NamedTuple):
    value: int
    direction: Direction = None
    turn: Turn = None
    move: Move = None

def parse_instruction(instruction):
    code = instruction[0]
    value = int(instruction[1:])
    if code == 'F':
        return Inst(move=Move.F, value=value)
    if code in ('L', 'R'):
        return Inst(turn=Turn(code), value=value)
    return Inst(direction=Direction(code), value=value)

ass(Inst(move=Move.F, value=10), parse_instruction, "F10")
ass(Inst(turn=Turn.R, value=90), parse_instruction, "R90")
ass(Inst(direction=Direction.N, value=3), parse_instruction, "N3")

def parse_instructions(lines):
    return [parse_instruction(line) for line in lines]

DIRECTION_TO_COORDINATE_CHANGE = {
    Direction.N: (0, 1),
    Direction.E: (1, 0),
    Direction.S: (0, -1),
    Direction.W: (-1, 0),
}

def simulate(instructions):
    x, y, direction = 0, 0, Direction.E
    for instruction in instructions:
        if instruction.direction is not None or instruction.move is not None:
            dx, dy = DIRECTION_TO_COORDINATE_CHANGE[direction]
            if instruction.direction is not None:
                dx, dy = DIRECTION_TO_COORDINATE_CHANGE[instruction.direction]
            x += dx * instruction.value
            y += dy * instruction.value

        if instruction.turn is not None:
            if instruction.value % 90 != 0:
                raise ValueError(f"Got {instruction.value}, expected turn to be divisible by 90")
            turn_shift = instruction.value // 90 * instruction.turn.to_sign()
            direction = direction.cycle(turn_shift)

    return abs(x) + abs(y)

TEST_INSTRUCTIONS = parse_instructions("""F10
N3
F7
R90
F11""".split())

ass(25, simulate, TEST_INSTRUCTIONS)


def rotate(x, y, turn):
    turn = turn % 4
    while turn > 0:
        x, y = y, -x
        turn -= 1

    return x, y

ass((-2, 1), rotate, 1, 2, -1)
ass((2, -1), rotate, 1, 2, -3)

def simulate_waypoint(instructions):
    # Ship coords.
    s_x, s_y = 0, 0

    # Waypoint coords.
    w_x, w_y = 10, 1

    for instruction in instructions:
        if instruction.direction is not None:
            dx, dy = DIRECTION_TO_COORDINATE_CHANGE[instruction.direction]
            w_x += instruction.value * dx
            w_y += instruction.value * dy

        if instruction.turn is not None:
            if instruction.value % 90 != 0:
                raise ValueError(f"Got {instruction.value}, expected turn to be divisible by 90")
            turn_shift = instruction.value // 90 * instruction.turn.to_sign()
            w_x, w_y = rotate(w_x, w_y, turn_shift)

        if instruction.move is not None:
            s_x += instruction.value * w_x
            s_y += instruction.value * w_y

    return abs(s_x) + abs(s_y)

ass(286, simulate_waypoint, TEST_INSTRUCTIONS)


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        instructions = parse_instructions(lines)
        print(simulate(instructions))
        print(simulate_waypoint(instructions))


if __name__ == "__main__":
    main()
