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

class Turn(Enum):
    L = 'L'
    R = 'R'

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

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]


if __name__ == "__main__":
    main()
