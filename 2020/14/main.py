from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class Mask():
    def __init__(self, value: str):
        # We need to preserve all X bits of the number, so we replace the X
        # bits with a neutral element for the operation. Application is just
        # combining the number with the setters.
        self._zero_setter = int(value.replace('X', '1'), 2)
        self._one_setter = int(value.replace('X', '0'), 2)

    def apply(self, value: int) -> int:
        return value & self._zero_setter | self._one_setter

ass(73, Mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X").apply, 11)
ass(101, Mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X").apply, 101)


class Assignment(NamedTuple):
    location: int
    value: int

class Statement(NamedTuple):
    mask_update: Mask = None
    assignment: Assignment = None

LEFT_SQUARE_BRACKET = '['
RIGHT_SQUARE_BRACKET_GROUP = "] = "

def parse_assignment(line: str) -> Assignment:
    left = line.find(LEFT_SQUARE_BRACKET)
    right = line.find(RIGHT_SQUARE_BRACKET_GROUP)
    location = int(line[left + 1 : right])
    value = int(line[right + len(RIGHT_SQUARE_BRACKET_GROUP):])
    return Assignment(location=location, value=value)

ass(Assignment(location=8, value=11), parse_assignment, 'mem[8] = 11')
ass(Assignment(location=7, value=101), parse_assignment, 'mem[7] = 101')

MASK_PREFIX = 'mask = '

def parse_program(lines: List[str]) -> List[Statement]:
    result = []
    for line in lines:
        if line.startswith(MASK_PREFIX):
            result.append(Statement(mask_update=Mask(line[len(MASK_PREFIX):])))
        else:
            result.append(Statement(assignment=parse_assignment(line)))

    return result

def evaluate_program(statements: List[Statement]) -> int:
    memory = dict()
    mask = None
    for statement in statements:
        if statement.mask_update is not None:
            mask = statement.mask_update
        else:
            memory[statement.assignment.location] = mask.apply(statement.assignment.value)
    return sum(value for value in memory.values())


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        statements = parse_program(lines)
        print(evaluate_program(statements))


if __name__ == "__main__":
    main()
