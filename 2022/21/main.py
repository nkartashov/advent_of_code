from typing import (
    List,
    NamedTuple,
    Tuple,
    Dict,
    Union,
    Deque,
    Set,
    Optional,
    Iterable,
    FrozenSet,
)
from enum import Enum
from collections import deque
from itertools import product, combinations, chain
import traceback
import tqdm
import time
import math

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")


TEST_DATA = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".split(
    "\n"
)

ROOT = "root"

Value = Union[int, str]


class OpKind(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class Op(NamedTuple):
    left: Value
    op: OpKind
    right: Value


class Monkey(NamedTuple):
    name: str
    value: Union[Op, Value]


def parse_value(value: str) -> Value:
    try:
        return int(value)
    except ValueError:
        return value


def parse_monkey(line: str) -> Monkey:
    name, rest = line.split(": ")
    parts = rest.split()
    if len(parts) == 1:
        return Monkey(name=name, value=parse_value(parts[0]))

    return Monkey(
        name=name,
        value=Op(
            left=parse_value(parts[0]), op=OpKind(parts[1]), right=parse_value(parts[2])
        ),
    )


def parse_monkeys(lines: List[str]) -> List[Monkey]:
    return [parse_monkey(line) for line in lines]


def resolve(name: str, monkeys: Dict[str, Monkey], computed: Dict[str, int]) -> int:
    def resolve_arg(arg: Value) -> int:
        if isinstance(arg, str):
            return resolve(arg, monkeys, computed)

        return arg

    if name not in computed:
        value = monkeys[name].value
        if isinstance(value, Op):
            left = resolve_arg(value.left)
            right = resolve_arg(value.right)
            if value.op == OpKind.ADD:
                computed[name] = left + right
            if value.op == OpKind.SUB:
                computed[name] = left - right
            if value.op == OpKind.MUL:
                computed[name] = left * right
            if value.op == OpKind.DIV:
                computed[name] = left // right
        else:
            computed[name] = resolve_arg(value)

    return computed[name]


def solve1(lines: List[str]) -> int:
    monkeys = {m.name: m for m in parse_monkeys(lines)}
    computed = {}
    return resolve(ROOT, monkeys, computed)


assrt(152, solve1, TEST_DATA)

HUMN = "humn"


def solve2(lines: List[str]) -> int:
    monkeys = {m.name: m for m in parse_monkeys(lines)}

    def resolve(name: str, humn_value: int, computed: Dict[str, int]) -> int:
        if name == HUMN:
            return humn_value

        def resolve_arg(arg: Value) -> int:
            if isinstance(arg, str):
                return resolve(arg, humn_value, computed)

            return arg

        if name not in computed:
            value = monkeys[name].value
            if isinstance(value, Op):
                left = resolve_arg(value.left)
                right = resolve_arg(value.right)

                if name == ROOT:
                    computed[name] = abs(left - right)
                    return computed[name]

                if value.op == OpKind.ADD:
                    computed[name] = left + right
                if value.op == OpKind.SUB:
                    computed[name] = left - right
                if value.op == OpKind.MUL:
                    computed[name] = left * right
                if value.op == OpKind.DIV:
                    computed[name] = left // right
            else:
                computed[name] = resolve_arg(value)

        return computed[name]

    left = -10 * 10**20
    # Cheeky -1 to deal with integer division problems somewhere
    # which curiously fails the test data check.
    right = 10 * 10**20 - 1
    l = resolve(ROOT, left, {})
    r = resolve(ROOT, right, {})
    while left < right:
        mid = left + (right - left) // 2
        computed = {}
        m = resolve(ROOT, mid, computed)

        if m == 0:
            return mid

        if r < l:
            left = mid
            l = m
        else:
            right = mid
            r = m

    assert False


assrt(301, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
