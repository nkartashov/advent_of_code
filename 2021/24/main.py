from re import S
from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any, FrozenSet
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import Error, deepcopy
from itertools import product, combinations
from functools import lru_cache
import math
from typing_extensions import ParamSpecArgs
from sortedcontainers import SortedDict
import functools
import operator
from tqdm import tqdm


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


Z = "z"
VARIABLE_TO_LABEL = ["w", "x", "y", Z]


class Val(NamedTuple):
    value: int


class Var(NamedTuple):
    label: int


class IType(Enum):
    INP = "inp"
    ADD = "add"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    EQL = "eql"
    NEQ = "neq"


class Instruction(NamedTuple):
    t: IType
    x: Var
    y: Optional[Union[Val, Var]] = None


def parse_var(var_text: str) -> Var:
    label = VARIABLE_TO_LABEL.index(var_text)
    return Var(label=label)


class InputTerm(NamedTuple):
    label: int

    def __repr__(self):
        return f"i{self.label}"


class Literal(NamedTuple):
    value: int

    def __repr__(self):
        return str(self.value)


Term = Union["OpTerm", "MemoryTerm", Literal, InputTerm]


class MemoryTerm(NamedTuple):
    name: str
    generation: int
    term: Term

    def __repr__(self):
        return f"{self.name}{self.generation}"


class OpTerm(NamedTuple):
    t: IType
    terms: List[Term]

    def __repr__(self):
        assert self.t != IType.INP

        op = "+"
        if self.t == IType.MUL:
            op = "*"
        if self.t == IType.DIV:
            op = "/"
        if self.t == IType.MOD:
            op = "%"
        if self.t == IType.EQL:
            op = "=="
        if self.t == IType.NEQ:
            op = "!="

        assert len(self.terms) == 2

        op = " " + op + " "

        return op.join(
            f"({term})" if isinstance(term, OpTerm) else f"{term}"
            for term in self.terms
        )


def parse_instruction(line: str) -> Instruction:
    s = line.split("#")
    if len(s) > 0:
        line = s[0]

    instruction_text, rest = line.split(" ", maxsplit=1)
    t = IType(instruction_text)
    if t == IType.INP:
        return Instruction(t=t, x=parse_var(rest))

    x_text, y_text = rest.split()
    return Instruction(
        t=t,
        x=parse_var(x_text),
        y=parse_var(y_text) if y_text in VARIABLE_TO_LABEL else Val(value=int(y_text)),
    )


def parse_instructions(lines: List[str]) -> List[Instruction]:
    return [parse_instruction(line) for line in lines]


def parse_input() -> List[Instruction]:
    with open("in.txt") as infile:
        return parse_instructions(
            [line.strip() for line in infile.readlines() if line.strip()]
        )


def run(inputs: List[int], instructions: List[Instruction]) -> List[int]:
    state = [0] * len(VARIABLE_TO_LABEL)
    input_idx = 0

    def get_second_value(i: Instruction) -> int:
        assert i.y is not None
        if isinstance(i.y, Var):
            return state[i.y.label]

        assert isinstance(i.y, Val)
        return i.y.value

    for i in instructions:
        if i.t == IType.INP:
            state[i.x.label] = inputs[input_idx]
            input_idx += 1
            continue

        x = state[i.x.label]
        y = get_second_value(i)
        res = 0
        if i.t == IType.ADD:
            res = x + y
        if i.t == IType.MUL:
            res = x * y
        if i.t == IType.DIV:
            res = x // y
        if i.t == IType.MOD:
            res = x % y
        if i.t == IType.EQL:
            res = 1 if x == y else 0
        state[i.x.label] = res
    return state


LITERAL_ZERO = Literal(value=0)
LITERAL_ONE = Literal(value=1)

MIN_VAR_VALUE = 1
MAX_VAR_VALUE = 10


def is_zero(x):
    return isinstance(x, Literal) and x == LITERAL_ZERO


def is_one(x):
    return isinstance(x, Literal) and x == LITERAL_ONE


def find_term_expressions(instructions: List[Instruction]) -> List[Term]:
    state: List[Term] = [Literal(value=0) for _ in VARIABLE_TO_LABEL]
    input_idx = 0

    def get_term(x):
        assert x is not None
        if isinstance(x, Var):
            return state[x.label]

        assert isinstance(x, Val)
        return Literal(value=x.value)

    def make_term(t, x, y):
        if t == IType.ADD:
            if is_zero(x):
                return y
            if is_zero(y):
                return x

        if t == IType.MUL:
            if is_zero(x) or is_zero(y):
                return LITERAL_ZERO

            if is_one(x):
                return y
            if is_one(y):
                return x

        if t == IType.DIV:
            if is_zero(x):
                return LITERAL_ZERO

            if is_one(y):
                return x

        if t == IType.MOD:
            if is_zero(x):
                return LITERAL_ZERO

            if is_one(y):
                return LITERAL_ZERO

        if t == IType.EQL:
            if (
                isinstance(x, InputTerm)
                and isinstance(y, Literal)
                and not (0 < y.value < 9)
            ):
                return LITERAL_ZERO
            if (
                isinstance(y, InputTerm)
                and isinstance(x, Literal)
                and not (0 < x.value < 9)
            ):
                return LITERAL_ZERO
            if (
                isinstance(x, OpTerm)
                and x.t == IType.EQL
                and isinstance(y, Literal)
                and y.value == 0
            ):
                return OpTerm(t=IType.NEQ, terms=x.terms)

        if isinstance(x, Literal) and isinstance(y, Literal):
            res = 0
            if t == IType.ADD:
                res = x.value + y.value
            if t == IType.MUL:
                res = x.value * y.value
            if t == IType.DIV:
                res = x.value // y.value
            if t == IType.MOD:
                res = x.value % y.value
            if t == IType.EQL:
                res = 1 if x.value == y.value else 0
            return Literal(value=res)

        return OpTerm(t=t, terms=[x, y])

    history = []

    def simplify_z(z):
        assert isinstance(z, OpTerm)
        assert z.t == IType.ADD
        left, right = z.terms
        assert isinstance(right, OpTerm)
        assert right.t == IType.MUL

        assert isinstance(left, OpTerm)
        assert left.t == IType.MUL

        iterm = right.terms[0]
        zterm = None
        if isinstance(left.terms[0], MemoryTerm):
            zterm = OpTerm(t=IType.MUL, terms=[Literal(value=26), left.terms[0]])
            zterm = OpTerm(t=IType.ADD, terms=[zterm, iterm])
        else:
            assert isinstance(left.terms[0], OpTerm)
            assert left.terms[0].t == IType.DIV
            zterm = history[input_idx - 2][1][0]  # 26 * z + i + 5

            assert isinstance(zterm, OpTerm)
            assert zterm.t == IType.ADD

            assert isinstance(zterm.terms[0], OpTerm)
            zterm = zterm.terms[0]  # 26 * z
            assert zterm.t == IType.MUL
            assert isinstance(zterm.terms[1], MemoryTerm)
            zterm = zterm.terms[1]
            zterm = history[zterm.generation - 1][1][0]
            assert isinstance(zterm, OpTerm)

        assert isinstance(right.terms[1], OpTerm)
        assert isinstance(right.terms[1].terms[0], OpTerm)
        assert right.terms[1].terms[0].t == IType.ADD
        left_of_neq_sign = right.terms[1].terms[0]
        right_of_neq_sign = right.terms[1].terms[1]
        assert isinstance(right_of_neq_sign, InputTerm)
        assert isinstance(left_of_neq_sign.terms[1], Literal)
        val = left_of_neq_sign.terms[1].value
        req = None
        if val < 0:
            old_zterm = history[input_idx - 2][1][0]
            assert isinstance(old_zterm, OpTerm)
            assert old_zterm.t == IType.ADD

            old_iterm = old_zterm.terms[1]
            assert isinstance(old_iterm, OpTerm)
            assert old_iterm.t == IType.ADD
            assert isinstance(old_iterm.terms[1], Literal)
            req = OpTerm(
                t=IType.EQL,
                terms=[
                    OpTerm(
                        t=IType.ADD,
                        terms=[
                            old_iterm.terms[0],
                            Literal(value=old_iterm.terms[1].value + val),
                        ],
                    ),
                    right_of_neq_sign,
                ],
            )

        return (zterm, req)

    for i in instructions:
        if i.t == IType.INP:
            # Replace the state with memory terms.
            if input_idx != 0:
                history.append((state[-1], simplify_z(state[-1])))
            state[-1] = MemoryTerm(name=Z, generation=input_idx, term=state[-1])

            state[i.x.label] = InputTerm(label=input_idx)
            input_idx += 1
            continue

        x = get_term(i.x)
        y = get_term(i.y)
        state[i.x.label] = make_term(i.t, x, y)

    history.append((state[-1], simplify_z(state[-1])))
    return state, history


# z13 - 10 == i13
# z12 - 8 == i12
# z11 > 0
# z12 > 0

# z0 = 0
# z1 = 26 * z0 + i0 + 7
# z2 = 26 * z1 + i1 + 15
# z3 = 26 * z2 + i2 + 2
# i2 - 1 != i3: True: z4 = z2 * 26 + i3 + 15
#               False: z4 = z2
# z5 = 26 * z4 + i4 + 14
# i4 + 5 != i5: True: z6 = z2 * 26 + i5 + 2
#               False: z6 = z2


def solve1(instructions: List[Instruction]) -> int:
    inputs = [6, 5, 9, 8, 4, 9, 1, 9, 9, 9, 7, 9, 3, 9]
    state = run(inputs, instructions)
    valid = state[VARIABLE_TO_LABEL.index(Z)] == 0
    if valid:
        print("".join(str(i) for i in inputs))
    else:
        print("FAIL")


def solve2(instructions: List[Instruction]) -> int:
    inputs = [1, 1, 2, 1, 1, 6, 1, 9, 5, 4, 1, 7, 1, 3]
    state = run(inputs, instructions)
    valid = state[VARIABLE_TO_LABEL.index(Z)] == 0
    if valid:
        print("".join(str(i) for i in inputs))
    else:
        print("FAIL")


def main():
    instructions = parse_input()
    _, history = find_term_expressions(instructions)
    for h in history:
        req = h[1][1]
        if req is not None:
            print(req)
    solve1(instructions)
    solve2(instructions)


if __name__ == "__main__":
    main()
