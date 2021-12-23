from re import S
from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any
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


class Type(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Pod(NamedTuple):
    type: Type
    label: int

    def __repr__(self):
        return self.type.value


A1 = Pod(type=Type.A, label=0)
A2 = Pod(type=Type.A, label=0)
B1 = Pod(type=Type.B, label=0)
B2 = Pod(type=Type.B, label=0)
C1 = Pod(type=Type.C, label=0)
C2 = Pod(type=Type.C, label=0)
D1 = Pod(type=Type.D, label=0)
D2 = Pod(type=Type.D, label=0)

ROOM_TO_TYPE = [Type.A, Type.B, Type.C, Type.D]
TYPE_TO_ENERGY = {
    Type.A: 1,
    Type.B: 10,
    Type.C: 100,
    Type.D: 1000,
}

# First element is top, second is bottom.
BOTTOM = 1
TOP = 0
TEST_INPUT = [
    [B1, A1],
    [C1, D1],
    [B2, C2],
    [D2, A2],
]

INPUT = [
    [A1, D1],
    [C1, D2],
    [B1, A2],
    [B2, C2],
]

CORRIDOR_WIDTH = 11
ROOM_SPOTS = [2, 4, 6, 8]

BIG_NUMBER = 10 ** 10


def debug(state: List[Optional[Pod]], rooms: List[List[Optional[Pod]]]):
    lines = ["".join(str(x) if x is not None else "." for x in state)]
    for r in range(2):
        row = []
        for i in range(CORRIDOR_WIDTH):
            if i not in ROOM_SPOTS:
                row.append("#")
                continue

            idx = ROOM_SPOTS.index(i)
            spot = rooms[idx][r]
            row.append(str(spot) if spot is not None else ".")
        lines.append("".join(row))

    print("\n".join(lines))
    print()


def solve1(data: List[List[Pod]]) -> int:
    cache = dict()
    state: List[Optional[Pod]] = [None] * CORRIDOR_WIDTH

    def runner(
        state: List[Optional[Pod]], rooms: List[List[Optional[Pod]]]
    ) -> Optional[int]:
        if all(s is None for s in state) and all(
            all(x is not None and x.type == ROOM_TO_TYPE[i] for x in room)
            for i, room in enumerate(rooms)
        ):
            return 0

        key = tuple(state), tuple(tuple(room) for room in rooms)
        if key not in cache:
            result = BIG_NUMBER

            # Amphipod can exit a room.
            for i, room in enumerate(rooms):
                top, bottom = room
                if bottom is None:
                    # Room is empty.
                    continue

                to_move = None
                energy_to_leave = 0
                old_room = deepcopy(room)

                if top is None:
                    if bottom.type == ROOM_TO_TYPE[i]:
                        # Already in the right room.
                        continue

                    # Bottom is the one to move.
                    to_move = bottom
                    room[BOTTOM] = None
                    # Step into top and move to the spot in front of the room.
                    energy_to_leave = 2 * TYPE_TO_ENERGY[to_move.type]
                else:
                    if top.type == ROOM_TO_TYPE[i] and bottom.type == ROOM_TO_TYPE[i]:
                        # The whole room is finished.
                        continue

                    # Top is the one to move.
                    to_move = top
                    room[TOP] = None
                    # Move to the spot in front of the room.
                    energy_to_leave = TYPE_TO_ENERGY[to_move.type]
                assert to_move is not None

                start = ROOM_SPOTS[i]
                # Go right.
                step = 1
                while start + step < CORRIDOR_WIDTH and state[start + step] is None:
                    if start + step not in ROOM_SPOTS:
                        state[start + step] = to_move
                        # Room is already updated above.
                        subresult = runner(state, rooms)
                        state[start + step] = None
                        if subresult is not None:
                            result = min(
                                result,
                                # Energy to get out of the room.
                                energy_to_leave
                                # Energy to go right.
                                + TYPE_TO_ENERGY[to_move.type] * step
                                # Energy to finish the puzzle.
                                + subresult,
                            )
                    step += 1

                # Go left.
                step = 1
                while start - step >= 0 and state[start - step] is None:
                    if start - step not in ROOM_SPOTS:
                        state[start - step] = to_move
                        # Room is already updated above.
                        subresult = runner(state, rooms)
                        state[start - step] = None
                        if subresult is not None:
                            result = min(
                                result,
                                # Energy to get out of the room.
                                energy_to_leave
                                # Energy to go right.
                                + TYPE_TO_ENERGY[to_move.type] * step
                                # Energy to finish the puzzle.
                                + subresult,
                            )
                    step += 1

                rooms[i] = old_room

            # Amphipod can enter a room.
            for i, x in enumerate(state):
                if x is None:
                    # No amphipod there.
                    continue

                room_idx = ROOM_TO_TYPE.index(x.type)
                room = rooms[room_idx]
                old_room = deepcopy(room)
                top, bottom = room
                if top is not None or bottom is not None and bottom.type != x.type:
                    # Room is full or there is an amphipod of a different type there already.
                    continue

                # Energy to step from the room spot into the room.
                effort_to_enter = TYPE_TO_ENERGY[x.type]
                if bottom is None:
                    # We can go to the bottom of the room.
                    effort_to_enter *= 2
                    room[BOTTOM] = x
                else:
                    room[TOP] = x

                room_spot = ROOM_SPOTS[room_idx]
                s, e = i + 1, room_spot + 1
                if room_spot < i:
                    s, e = room_spot, i
                if all(y is None for y in state[s:e]):
                    # Path is clear.
                    state[i] = None
                    subresult = runner(state, rooms)
                    if subresult is not None:
                        result = min(
                            result,
                            # Energy to enter the room from its spot.
                            effort_to_enter
                            # Energy to get to the spot.
                            + (e - s) * TYPE_TO_ENERGY[x.type]
                            # Energy to finish the puzzle.
                            + subresult,
                        )

                state[i] = x
                rooms[room_idx] = old_room

            if result == BIG_NUMBER:
                # We couldn't do anything.
                result = None
            cache[key] = result

        return cache[key]

    result = runner(state, data)
    assert result is not None
    return result


assrt(12521, solve1, TEST_INPUT)


def main():
    print(solve1(INPUT))


if __name__ == "__main__":
    main()
