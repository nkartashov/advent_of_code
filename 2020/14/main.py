from typing import List, NamedTuple, Set
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class Mask():
    def __init__(self, value: str):
        self._original = value
        # We need to preserve all X bits of the number, so we replace the X
        # bits with a neutral element for the operation. Application is just
        # combining the number with the setters.
        self._zero_setter = int(value.replace('X', '1'), 2)
        self._one_setter = int(value.replace('X', '0'), 2)

    def apply(self, value: int) -> int:
        return value & self._zero_setter | self._one_setter

    def apply_floating_mask(self, location: int) -> str:
        location_string = f'{location:036b}'
        def mixer(location_bit, mask_bit):
            if mask_bit == '0':
                return location_bit
            # If the mask bit is 1, address bit is ovewritten with 1.
            return mask_bit

        return ''.join(mixer(location_string[i], mask_bit) for i, mask_bit in enumerate(self._original))

ass(73, Mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X").apply, 11)
ass(101, Mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X").apply, 101)

ass('000000000000000000000000000000X1101X', Mask('000000000000000000000000000000X1001X').apply_floating_mask, 42)


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

def generate_updates_from_mask(mask: str) -> Set[str]:
    result = set()
    buf = []
    def generator(i):
        if i == len(mask):
            result.add(''.join(buf))
            return

        values = [mask[i]]
        if mask[i] == 'X':
            values = ['0', '1']
        for value in values:
            buf.append(value)
            generator(i + 1)
            buf.pop()

    generator(0)
    return result

class FloatingUpdate:
    mask: str
    value: int

    def __init__(self, *, mask, value):
        self._mask = mask
        self._value = value
        self._generated_updates = generate_updates_from_mask(self._mask)

    def does_intersect(self, other: 'FloatingUpdate') -> bool:
        def bits_intersect(left, right):
            return left == right or 'X' in (left, right)

        return all(bits_intersect(l, r) for l, r in zip(self._mask, other._mask))

    def remove_updates(self, other: 'FloatingUpdate'):
        if self.does_intersect(other):
            self._generated_updates = self._generated_updates - other._generated_updates
    
    @property
    def contribution(self):
        return len(self._generated_updates) * self._value


def evaluate_program2(statements: List[Statement]) -> int:
    result = 0
    updates = []
    mask = None
    for statement in statements:
        if statement.mask_update is not None:
            mask = statement.mask_update
        else:
            update_mask = mask.apply_floating_mask(statement.assignment.location)
            updates.append(FloatingUpdate(mask=update_mask, value=statement.assignment.value))

    updates.reverse()
    for i, update in enumerate(updates):
        for j in range(0, i):
            update.remove_updates(updates[j])
        result += update.contribution

    return result

TEST_PROGRAM = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split('\n')
ass(208, evaluate_program2, parse_program(TEST_PROGRAM))


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        statements = parse_program(lines)
        print(evaluate_program(statements))
        print(evaluate_program2(statements))


if __name__ == "__main__":
    main()
