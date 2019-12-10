import copy
from typing import NamedTuple, Any, List
from enum import Enum


def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class ArgMode(Enum):
    POSITION = 0
    IMMEDIATE = 1

class OpCode(Enum):
    SUM = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JNZ = 5
    JZ = 6
    LT = 7
    EQ = 8
    HALT = 99


ARG_COUNTS = {
    OpCode.SUM: 3,
    OpCode.MULT: 3,
    OpCode.INPUT: 1,
    OpCode.OUTPUT: 1,
    OpCode.JNZ: 2,
    OpCode.JZ: 2,
    OpCode.LT: 3,
    OpCode.EQ: 3,
    OpCode.HALT: 0,
}

ARITHMETIC_OPS = {OpCode.SUM, OpCode.MULT}
JUMP_OPS = {OpCode.JZ, OpCode.JNZ}
LOGIC_OPS = {OpCode.LT, OpCode.EQ}
BINARY_OPS = ARITHMETIC_OPS | LOGIC_OPS

class Op(NamedTuple):
    op: OpCode
    arg_modes: List[ArgMode]

    @property
    def arg_count(self):
        return ARG_COUNTS[self.op]

    def _get_arg_value(self, memory, pc, arg_idx):
        mode = self.arg_modes[arg_idx]
        result = memory[pc + arg_idx + 1]
        if mode == ArgMode.POSITION:
            result = memory[result]
        return result

    def _get_dest_arg(self, memory, pc):
        return memory[pc + self.arg_count]

    def _get_first_arg(self, memory, pc):
        return self._get_arg_value(memory, pc, 0)

    def _get_second_arg(self, memory, pc):
        return self._get_arg_value(memory, pc, 1)

    def run(self, memory, pc, inputs, outputs):
        new_pc = pc + self.arg_count + 1
        if self.op == OpCode.HALT:
            return -1
        if self.op in BINARY_OPS:
            a = self._get_first_arg(memory, pc)
            b = self._get_second_arg(memory, pc)
            dest = self._get_dest_arg(memory, pc)
            result = a + b
            if self.op == OpCode.MULT:
                result = a * b
            if self.op == OpCode.LT:
                result = 1 if a < b else 0
            if self.op == OpCode.EQ:
                result = 1 if a == b else 0
            memory[dest] = result
            return new_pc

        if self.op in JUMP_OPS:
            cond = self._get_first_arg(memory, pc)
            if (cond == 0) == (self.op == OpCode.JZ):
                new_pc = self._get_second_arg(memory, pc)

        if self.op == OpCode.INPUT:
            memory[self._get_dest_arg(memory, pc)] = inputs.pop() 
        if self.op == OpCode.OUTPUT:
            outputs.append(self._get_first_arg(memory, pc))

        return new_pc

def read_op(value):
    op = OpCode(value % 100)
    value //= 100
    arg_modes = []
    for _ in range(ARG_COUNTS[op]):
        arg_modes.append(ArgMode(value % 10))
        value //= 10
    return Op(op=op, arg_modes=arg_modes)

ass(
    Op(op=OpCode.MULT, arg_modes=[ArgMode.POSITION, ArgMode.IMMEDIATE, ArgMode.POSITION]),
    read_op,
    1002,
) 

def eval_program2(memory, inputs):
    memory = copy.deepcopy(memory)
    pc = 0
    outputs = []
    while pc != -1:
        op = read_op(memory[pc])
        pc = op.run(memory, pc, inputs, outputs)
    return memory, outputs

ass(([2,0,0,0,99], []), eval_program2, [1,0,0,0,99], [])
ass(([30,1,1,4,2,5,6,0,99], []), eval_program2, [1,1,1,4,99,5,6,0,99], [])

def eval_for_output(memory, inputs):
    _, outputs = eval_program2(memory, inputs)
    return outputs

ass(([3,9,8,9,10,9,4,9,99,1,8], [1]), eval_program2, [3,9,8,9,10,9,4,9,99,-1,8], [8])
ass([1], eval_for_output, [3,9,8,9,10,9,4,9,99,-1,8], [8])
ass([1], eval_for_output, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [7])


def main():
    with open('in.txt') as infile:
        state = [int(code) for code in infile.read().strip().split(',')]
        memory1, outputs1 = eval_program2(state, [1])
        memory2, outputs2 = eval_program2(state, [5])
        print(outputs1)
        print(outputs2)


if __name__ == "__main__":
    main()
