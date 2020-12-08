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

    def flip_nop_jmp(self):
        if self.op == Op.acc:
            raise ValueError()

        result_op = Op.nop
        if self.op == Op.nop:
            result_op=Op.jmp
        return Inst(op=result_op, arg=self.arg)

def parse_instruction(line):
    op, arg = line.split()
    return Inst(op=Op(op), arg=int(arg))

assert(parse_instruction("nop +0") == Inst(op=Op.nop, arg=0))
assert(parse_instruction("acc -99") == Inst(op=Op.acc, arg=-99))

def parse_instructions(lines):
    return [parse_instruction(line) for line in lines]


def run_program_until_loop(instructions, possible_break_idx=None):
    cnt = 0
    acc = 0
    visited = set()
    visited_nops_jmps = set()
    while True:
        if cnt == len(instructions):
            break

        if cnt in visited:
            if possible_break_idx is not None:
                return None
            return acc, visited_nops_jmps

        visited.add(cnt)
        inst = instructions[cnt]

        if possible_break_idx == cnt:
            inst = inst.flip_nop_jmp()

        if inst.op == Op.nop:
            if inst.arg != 0:
                # Don't need 0 jumps.
                visited_nops_jmps.add(cnt)
            cnt += 1
        elif inst.op == Op.jmp:
            visited_nops_jmps.add(cnt)
            cnt += inst.arg
        elif inst.op == Op.acc:
            cnt += 1
            acc += inst.arg
        else:
            raise ValueError()

    return acc

def try_repair_and_run(instructions, visited_nops_jmps):
    for possible_break_idx in visited_nops_jmps:
        result = run_program_until_loop(instructions, possible_break_idx=possible_break_idx)
        if result is not None:
            return result
    return None
        

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        instructions = parse_instructions(lines)
        solution, visited_nops_jmps = run_program_until_loop(instructions)
        print(solution)
        print(try_repair_and_run(instructions, visited_nops_jmps))


if __name__ == "__main__":
    main()
