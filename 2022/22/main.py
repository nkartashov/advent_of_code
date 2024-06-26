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


class Tile(Enum):
    EMPTY = "."
    WALL = "#"
    SPACE = " "


class Row:
    def __init__(self, row: List[Tile], first_non_space: int):
        self._row = row
        self._first_non_space = first_non_space

    @property
    def first_non_space(self) -> int:
        return self._first_non_space

    def __getitem__(self, i: int) -> Tile:
        return self._row[i]

    def __len__(self) -> int:
        return len(self._row)


class Map:
    def __init__(self, rows: List[Row]):
        self._rows = rows
        first_non_space_column = [None] * max(len(row) for row in rows)
        for j, row in enumerate(rows):
            for i, x in enumerate(row._row):
                if first_non_space_column[i] is None and x != Tile.SPACE:
                    first_non_space_column[i] = j

        self._first_non_space_by_column = first_non_space_column

    def __getitem__(self, j: int) -> Row:
        return self._rows[j]

    def get(self, i: int, j: int, facing: Tuple[int, int]) -> Tile:
        dx, dy = facing
        x = i + dx
        y = j + dy
        pass


def parse_map(lines: List[str]) -> Map:
    rows = []
    for line in lines:
        i = 0
        while line[i] != Tile.SPACE.value:
            i += 1
        rows.append(Row(row=[Tile(x) for x in line], first_non_space=i))
    return Map(rows=rows)


L = "L"
R = "R"


def parse_directions(directions: str) -> List[Union[int, str]]:
    result = []
    i = 0
    while i < len(directions):
        number_length = 1
        while i + number_length < len(directions) and directions[
            i + number_length
        ] not in {L, R}:
            number_length += 1
        result.append(int(directions[i : i + number_length]))
        result.append(directions[i + number_length])
        i += number_length + 1

    return result


DIRECTIONS = "28L12L22R45R42R33L19L16R46R14R32L45L9R9R26L36L31R7R9L41R43R36L18L5R47R37L31L14R25L19L17R4R19R15L24R12L28R22R18R33R41R14R20L1R45L25R41L37L24L45L4L35R13L15R36L44R49R39R48L34R22R14R42R37L34R33R10R3L11R12R40R13L19R1R25L12R5R4R36R29R27L45R42L37R35L50L31R37L46L37L16R7R12R45R36R5R21L30R23R33L13R43R22R5R4R8L35L46L42R45R34R14R1L25R1L34R39L14L31L4L21L24R50R39L23L12L11L7R1R12R26L25R31L43R7R5L26L49R47R47R40R18R41R9R12R19R41L21R34R10L31L42R29R50R2R42L12R28R35L17L5L32R6R18R28L11L44R16L31R28R7R4R39R2L22R14R20R44L23L30L19R10R48L43L14R41R11R14L48R12R19L7L22L16R4R1L50L18L47L27L7L13R8L32L20L32L43R43R29L27L36R4L42R9L40R29L40R29L2L21R5L45L9R34R2L39R42R50L46L11R21R7L18L20R4R10R14L16R21L19L6L42R37R48R35R38L31L3R35L40R12L46L18L40R46R39R33L23R25R26R3L39L50R6L7L15L32L41L6L6L37R34R4R11R4L38R2R45R9L5L45L4R17L4L6R23R35R15R21R44R48R47L42L34R37L22L3R20L6R18L17L33L16R11R6R19L4R39L23R35L26R35L5R16R28L10L2L22L27L28L37R4R18L9R31L9R26L30R2R37L9R3L41L15R11L43L23R41R19R37L22R18R18R40L14R21R43R22R46L29L17R7R25R9R38L27R9R16L16R21R46R36L12L22R42R9L9R32R14L26R36R39L46L31R36L8R35L2L24L34R47R14R1R42R27L17L8R38R16R19L4R9L28L3L47R18R25R42R44R49R9R7L4L30L5R11L33L31L44L35L18L41L46L8L44R1R10R46R27R17L44L26R29L44R3R46R41R18R5R49L24R1R2R4L44L42L27R36L23L25R2L7L9L13L4L46R18R1R18R42L23R49L49L39R34L42L8L24L23R17R48R17R17R14R1L9R34L37R24R32R49L16R36R43R23L29R44R23R40L49L27L13R31L24R19L7R42L25L4R29L29L16L22R2L6L26R44R21L42R6R21L31L9L38L27R1R41L27L6R12R36R43R20L24R43R34L15R4L38R28L23L36L35L31L9L2L3L45L26R45R36R25R48R5L50R38L22L26R37R16R21R44L10R32R15R2L17R43R11R10L21R9R30R11R37R7R32L43L24L18L40R12L45R23R44L3L25R8L48R12L21R48R41L4L26R42R17L9L49R8R13R7R12R33L47L37R5L1R45L32L28R13R27R48R40R23R20L6R5R9L43R39L39R8L30L36L2L17R21R23L8L23L24R40R30R10L39R48R46R24R29L16R20L10L46L19L24R29R45R40R15R26L1R7L50R9L30L8L20L16R40L34R31L21R36L36R27R1L15R28L28L45R10L7L16R13L44R28L34L40L32R5R22R24L24R48L2R6L19R48L47R27L31L49R33R35L21R41R36L32L40R20L15R10R33L21L16R14R2L31R7L19L42R16R40R21L44R37L30L19L5L36L16R44R48R16R32L27R47L13L33L22L6R1R24L21R49L26R46R28L34L11L10L26L2R2L50L25R49R23R6R16L11R6R20L2L45R3R29L29R46R34L9L27R24L16L28L28L19L6L10L38L3R19R29L13R36L29R24L27R32R22L14R20L36R20L26R29L1L43L7R42R4L32R7L41L17R27R40R39R25L32L50R47R1R25L22L35L2R18L27L15L41L20L30L13R26L46R37R11L2R45R40R3L4R11R21R13L38R26R46L29R46L3R28L1L32R29R34L19R49L45R10R45R50R42L10R11L4R1R32L15L39L10R17L11R39L1L6L25R39R1R5L28R47R44L13L22R22R42R30R44L32L35L36R23L37R28L7L5R15L7L6R24L11L16R22R16L35L18L2L36R12L29R12L11R29R19L31R48R29L20L28R45R43L33R7L9L31R27L30R5L32R12L33L46L6L10R36L23R34R30L20L30L35L21L25L1L44R3L31R41L24R17L10R11R50R30L5R18L13L1R29L1R28R19R32R18L24R20R43R2L42R47L40L37L36R32R48R40R18R23R10R9R27R1R30R16R1R4L49R1R38R42L40R43L6R27R1L35R30R21L3L21L44R17R23R8R16L36R38L15R43R5L5R34L12R25L48L43R44R22L8R21R13L3L41R21L46L42L14L42R11R19L36L33L18R28R32L11R35R9R10R6R25R37R42L19R20L23R20L37L1L4R38R10L41L34L19L15L9L42L28L26L46R48R19L24L29R41L21R28R15L30L17L37L47L45L49R42L40R3L49L8L13R4L17R21R25L43R1R9L8R6R2R36L41R22L47R34R20R12R34L27L48L40L37R44L48L26L38L29L44L17R49L6L43R48R2L3L39R10R1L14R40L15L31R7L25L10L1L30L27L50R10R35L21L15R20L9R9R3R37L30L44L35R29L1L41L37R1L38R7L16R24R2R32L49L42L42L7R18R39L48L49R15L15L36R3R2R5L45L3L33L48L19R3L33L30L30L26R13L44R34L42L36L35R9R46R10R1R24L49L31R36R41L33L49R22R17R45R16L40L10R9R35L7L49L15R45L27R7L25R35R33R39R11R41L39L41R49R4L34R17R50R22R46L48R24R3L10R40R42R3R26R19R42R23R11L17R44L28L48R38L26L23L43L9L44R20L29R3L46L31L8R49R40R25R27L19R22R40L28R18L6L11L11L25R34R10R11L3L27L35L50L14L49R7R38R49R18L3L38R33R24R44L30L48L40R12L21L4R9L36R17L4R3L27L4L11R39L17L7R7R37R7R8L45R20R43L5L2L49L6R10L1R8L14R50R40R33R41L1R4R29L10L43R1R2R23L3L50R48R1R18R11R12L21R24L29R14R44L43L18R2R36R29R20L34L15R35R16L48R14L35L41L41R3R1L21L40R19L29R15L9R37R6R45L46L9R36L16R12L15R19L18L2R7R16L21L27L14L3L5R5L47R5L28L24L23L22R16R40R6L30R16L24L22L15R22L39R28R50R43L13R11L34L33L20L18L34R39L47R29R13L12L25L48L38R13R5L11R47R23L3R28L38R37L41L38R23R27R13R2L31L30L15L48L3R4L11R48R5L12R47R45L27R19L1L20R11L28L40L5L15R10L7L35L48L46L21R21L8L29R38L24R4L39L6L33L50L35L26R8L46L39R44R50L31R48R30R11R1L6R12L28R9L49R16R41L7R10R16R4R20R47L26R16R20R44R20R5L10R19L25L7L5R12L45R21L14R35L11R38L15R8R46L35R19L41R5R46L8L24R5L13L25L34L28L9L36L14R49L35R44R26L8L33L26R43L49L36R18R22L3R19L21L11L24L18R13R8R49R25L10L6R44R32R3L16R3L32L3R9R28L45L24R45L11R47L12R18L50R40R42L2R46R17R43R10R27L34L27R46L20L22L6R3L31R25R16L7L43R10L23R38L21L32L24L44L9R32R9L10R7R26L14L34L44L47R25R33R30R33R9L41R50R16R16R4R32L24R29R22R15L28R11R31R26L11L20R48L32L14R47L49R26R28R24L23L14L48R47R19R12R6L32L50R3R37L36R26R18R31L5L10L10R11L24L20R46R16R13L17L2R39R50L7L5R29R18R49L40L14R17R5L27L48R19L37L15L8R46R1L16R25L2R48R12L10R3R37L11R19R6L48R19R17R1L4L42R27L10R25R48L40L11R33L43L24L27L34R43L40L41L35L24R43R42R50L22L1L26L21L25L50L47R32R22R26R29R13L3R17L46R7R39L27R34R8R39R5R45R48L23R43R15R25R34R11R31L33R2L5L21R39R17R46R33R28L3L26L45L37L5L33R42R19R32L6L48R28L12R18L8R48R48L48R14L38R24L49R4L50R20L7L48R19R9L48R27L48L40R42L4R41R10R7L27L44L28R17R45R25R2L49L15R49R3L46L45L4L5L30L25R36R25L1R37R47R45R21R40R3L38R4R22R9R32R34R2R19L27R6L6R16L28R20R23R23L17R33L3R21L36R5R48R12R15R35L43R23L29R25L20L12R37R1L8L47L9L5L8R2R11L29R2R15R34R19R37L8R21L20L8L24L2L41L49L5R32R33R11L34L36L13R10L29L28L49R7L12R30L1R13R48R46L29R19R15R1R47L27L40L22L10R7R14R49L19L11R30R15L11R2R35L19R27L12L20R35R20R5R47R35R46L3L44R34R11L44R21L16R32L48L44L45L30R31R49L36L50R26L34L10R24L37L49L48L19R19L19R6L33R3R29L19R28L44L11L37R40L6L10R12L44R30L37R28L30L30L2L48L44L10R4L4R15L48R19R43R25R7L31L20L10L40L30L2R29L48R17R11R1L45R36L14L31R22R45L33R45L48R29R23L3L33R32R9L25R46R33L34R7R39R9L6L41L45L44R10R18R9R3L50L14R24R17R47L19R3R30L24L15R35L44R39L16R49R3L17"

FACING = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def eval_ending_position(position: List[int], facing: Tuple[int, int]) -> int:
    return 1000 * position[1] + 4 * position[0] + FACING.index(facing)


def solve1(lines: List[str], directions: str = DIRECTIONS) -> int:
    m = parse_map(lines)
    dirs = parse_directions(directions)
    position = [m[0].first_non_space, 0]
    facing = FACING[0]
    for step in dirs:
        if isinstance(step, str):
            facing_idx = FACING.index(facing)
            facing = FACING[facing_idx + (1 if step == "R" else -1) % len(FACING)]
            continue

        x, y = position


TEST_DATA = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.""".split(
    "\n"
)

TEST_DIRECTIONS = "10R5L5R10L4R5L5"


assrt(6032, solve1, TEST_DATA, TEST_DIRECTIONS)


def solve2(lines: List[str]) -> int:
    pass


assrt(301, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
