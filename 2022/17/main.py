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

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")


TEST_DATA = [""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""]


# Shape is a collections of points, every point is relative to the top right corner.
class Shape:
    def __init__(self, points: List[List[bool]]):
        self._points = points

    @property
    def height(self):
        return len(self._points)

    def can_go_down(self, reference: List[int], field: List[List[bool]]) -> bool:
        return self._can_go(reference, field, (0, -1))

    def can_go_left(self, reference: List[int], field: List[List[bool]]) -> bool:
        return self._can_go(reference, field, (-1, 0))

    def can_go_right(self, reference: List[int], field: List[List[bool]]) -> bool:
        return self._can_go(reference, field, (1, 0))

    def add(
        self,
        reference: List[int],
        field: List[List[bool]],
    ):
        x, y = reference
        for j, row in enumerate(self._points):
            for i, value in enumerate(row):
                field[j + y][i + x] = field[j + y][i + x] or value

        while not any(field[-1]):
            field.pop()

    def _can_go(
        self, reference: List[int], field: List[List[bool]], diff: Tuple[int, int]
    ) -> bool:
        dx, dy = diff
        x, y = reference
        for j, row in enumerate(self._points):
            for i, value in enumerate(row):
                new_x = x + dx + i
                new_y = y + dy + j
                if value and not (
                    # The new y point is above the bottom.
                    0 <= new_y
                    # The new x is within the field.
                    and 0 <= new_x < len(field[new_y])
                    # The field doesn't have a point already.
                    and not field[new_y][new_x]
                ):
                    return False

        return True


SHAPES = [
    Shape(
        [
            [True, True, True, True],
        ]
    ),
    Shape(
        [
            [False, True, False],
            [True, True, True],
            [False, True, False],
        ]
    ),
    Shape(
        [
            [True, True, True],
            [False, False, True],
            [False, False, True],
        ]
    ),
    Shape(
        [
            [True],
            [True],
            [True],
            [True],
        ]
    ),
    Shape(
        [
            [True, True],
            [True, True],
        ]
    ),
]


assrt(
    True,
    SHAPES[1].can_go_down,
    [4, 2],
    [
        [False, False, True, True, True, True, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
    ],
)

LEFT = "<"
RIGHT = ">"


def print_glass(glass: List[List[bool]]):
    print(
        "\n".join("".join(("#" if x else ".") for x in row) for row in reversed(glass))
    )


def simulate(jets: str, steps: int) -> int:
    # Row 0 is bottom.
    glass = []
    jet_counter = 0
    for step in tqdm.trange(steps):
        shape = SHAPES[step % len(SHAPES)]

        # Add 3 empty rows + empty rows for the shape.
        for _ in range(3 + shape.height):
            glass.append([False] * 7)

        reference = [2, len(glass) - shape.height]
        while True:
            jet = jets[jet_counter % len(jets)]

            # Jet pushes the rock.
            if jet == LEFT:
                if shape.can_go_left(reference, glass):
                    reference[0] -= 1
            else:
                if shape.can_go_right(reference, glass):
                    reference[0] += 1
            jet_counter += 1

            # Rock falls down.
            if shape.can_go_down(reference, glass):
                reference[1] -= 1
            else:
                shape.add(reference, glass)
                break

    return len(glass)


def solve1(lines: List[str], steps=2022) -> int:
    jets = lines[0]
    return simulate(jets, steps)


assrt(3068, solve1, TEST_DATA)


def flatten(l):
    return list(chain.from_iterable(l))


def serialize_glass(glass: List[List[bool]]) -> tuple:
    assert len(glass) >= 100
    return tuple(flatten(glass[-100:]))


def solve2(lines: List[str], steps: int = 1_000_000_000_000) -> int:
    cache = dict()

    jets = lines[0]
    # Row 0 is bottom.
    glass = []
    jet_counter = 0
    result = 0

    step = 0

    with tqdm.tqdm(total=steps) as pbar:
        while step != steps:
            shape_idx = step % len(SHAPES)
            jet_idx = jet_counter % len(jets)
            caching_key = None, shape_idx, jet_idx

            if len(glass) >= 100:
                caching_key = serialize_glass(glass), shape_idx, jet_idx

            if caching_key[0] is not None:
                if caching_key in cache:
                    (
                        last_step_encountered,
                        last_height_encountered,
                    ) = cache[caching_key]
                    step_diff = step - last_step_encountered
                    height_diff = len(glass) - last_height_encountered
                    steps_to_skip = steps - step
                    times_skip = steps_to_skip // step_diff

                    result += height_diff * times_skip
                    step += step_diff * times_skip
                    pbar.update(step_diff * times_skip)
                else:
                    cache[caching_key] = (
                        step,
                        len(glass),
                    )

            old_height = len(glass)
            shape = SHAPES[shape_idx]

            # Add 3 empty rows + empty rows for the shape.
            for _ in range(3 + shape.height):
                glass.append([False] * 7)

            reference = [2, len(glass) - shape.height]
            while True:
                jet = jets[jet_counter % len(jets)]

                # Jet pushes the rock.
                if jet == LEFT:
                    if shape.can_go_left(reference, glass):
                        reference[0] -= 1
                else:
                    if shape.can_go_right(reference, glass):
                        reference[0] += 1
                jet_counter += 1

                # Rock falls down.
                if shape.can_go_down(reference, glass):
                    reference[1] -= 1
                else:
                    shape.add(reference, glass)
                    break

            result += len(glass) - old_height
            step += 1
            pbar.update(step)

        return result


# assrt(15148, simulate, TEST_DATA[0], 10_000)
assrt(15148, solve2, TEST_DATA, 10_000)
# assrt(151434, simulate, TEST_DATA[0], 100_000)
assrt(151434, solve2, TEST_DATA, 100_000)
assrt(1514285714288, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        # assrt(150773, simulate, lines[0], 100_000)
        assrt(150773, solve2, lines, 100_000)
        print(solve2(lines))


if __name__ == "__main__":
    main()
