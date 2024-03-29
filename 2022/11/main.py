from typing import List, NamedTuple, Tuple, Dict, Union, Callable, Deque
from enum import Enum

from collections import deque
from copy import deepcopy
import math

from tqdm import tqdm


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class Op:
    @property
    def to_lambda(self) -> Callable[[int], int]:
        return lambda x: x


class SqOp(Op):
    @property
    def to_lambda(self) -> Callable[[int], int]:
        return lambda x: x * x


class AddOp(Op):
    def __init__(self, value: int):
        self._value = value

    @property
    def to_lambda(self) -> Callable[[int], int]:
        return lambda x: x + self._value


class MulOp(Op):
    def __init__(self, value: int):
        self._value = value

    @property
    def to_lambda(self) -> Callable[[int], int]:
        return lambda x: x * self._value


class Monkey:
    def __init__(
        self,
        items: List[int],
        op: Op,
        divisor: int,
        next_true: int,
        next_false: int,
    ):
        self._items = deque(reversed(items))
        self._op = op
        self._divisor = divisor
        self._next_true = next_true
        self._next_false = next_false

    def has_items(self) -> bool:
        return len(self._items) > 0

    def add_item(self, item: int):
        self._items.appendleft(item)

    def inspect(self, hard: bool) -> Tuple[int, int]:
        worry = self._items.pop()
        new_worry = self._op.to_lambda(worry)
        if not hard:
            new_worry //= 3
        return (
            new_worry,
            self._next_true if new_worry % self._divisor == 0 else self._next_false,
        )

    def __repr__(self) -> str:
        return str(self._items)


TEST_MONKEYS = [
    Monkey(items=[79, 98], op=MulOp(19), divisor=23, next_true=2, next_false=3),
    Monkey(
        items=[54, 65, 75, 74],
        op=AddOp(6),
        divisor=19,
        next_true=2,
        next_false=0,
    ),
    Monkey(items=[79, 60, 97], op=SqOp(), divisor=13, next_true=1, next_false=3),
    Monkey(items=[74], op=AddOp(3), divisor=17, next_true=0, next_false=1),
]


def go(monkeys: List[Monkey], hard, rounds) -> int:
    monkeys = deepcopy(monkeys)
    counts = [0] * len(monkeys)
    for _ in tqdm(range(rounds)):
        for i, monkey in enumerate(monkeys):
            while monkey.has_items():
                counts[i] += 1
                worry, idx = monkey.inspect(hard=hard)
                monkeys[idx].add_item(worry)

    x, y = list(sorted(counts, reverse=True))[:2]
    return x * y


def solve1(monkeys: List[Monkey]) -> int:
    return go(monkeys=monkeys, hard=False, rounds=20)


assrt(10605, solve1, TEST_MONKEYS)


INPUT_MONKEYS = [
    Monkey(
        items=[72, 64, 51, 57, 93, 97, 68],
        op=MulOp(19),
        divisor=17,
        next_true=4,
        next_false=7,
    ),
    Monkey(items=[62], op=MulOp(11), divisor=3, next_true=3, next_false=2),
    Monkey(
        items=[57, 94, 69, 79, 72],
        op=AddOp(6),
        divisor=19,
        next_true=0,
        next_false=4,
    ),
    Monkey(
        items=[80, 64, 92, 93, 64, 56],
        op=AddOp(5),
        divisor=7,
        next_true=2,
        next_false=0,
    ),
    Monkey(
        items=[70, 88, 95, 99, 78, 72, 65, 94],
        op=AddOp(7),
        divisor=2,
        next_true=7,
        next_false=5,
    ),
    Monkey(items=[57, 95, 81, 61], op=SqOp(), divisor=5, next_true=1, next_false=6),
    Monkey(items=[79, 99], op=AddOp(2), divisor=11, next_true=3, next_false=1),
    Monkey(items=[68, 98, 62], op=AddOp(3), divisor=13, next_true=5, next_false=6),
]


def solve2(monkeys: List[Monkey], rounds=10_000) -> int:
    return go(monkeys=monkeys, hard=True, rounds=rounds)


assrt(6 * 4, solve2, TEST_MONKEYS, 1)
assrt(99 * 103, solve2, TEST_MONKEYS, 20)
assrt(5204 * 5192, solve2, TEST_MONKEYS, 1000)


def main():
    with open("in.txt") as infile:
        print(solve1(INPUT_MONKEYS))
        print(solve2(INPUT_MONKEYS))


if __name__ == "__main__":
    main()
