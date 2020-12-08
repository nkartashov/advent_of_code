from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict

class Op(Enum):
    nop = "nop"
    jmp = "jmp"
    acc = "acc"

class Inst(NamedTuple):
    op: Op
    arg: int

def parse_instruction(line):
    op, arg = line.split()
    return Inst(op=Op(op), arg=int(arg))

assert(parse_instruction("nop +0") == Inst(op=Op.nop, arg=0))
assert(parse_instruction("acc -99") == Inst(op=Op.acc, arg=-99))

def parse_instructions(lines):
    return [parse_instruction(line) for line in lines]


def run_program_until_loop(instructions):
    cnt = 0
    visited = set()
    acc = 0
    while cnt not in visited:
        visited.add(cnt)
        inst = instructions[cnt]
        if inst.op == Op.nop:
            cnt += 1
        elif inst.op == Op.jmp:
            cnt += inst.arg
        elif inst.op == Op.acc:
            cnt += 1
            acc += inst.arg
        else:
            raise ValueError()
    return acc

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        instructions = parse_instructions(lines)
        print(run_program_until_loop(instructions))


if __name__ == "__main__":
    main()
