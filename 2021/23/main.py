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


A = "A"
B = "B"
C = "C"
D = "D"

ROOM_TO_TYPE = [A, B, C, D]
TYPE_TO_ENERGY = {
    A: 1,
    B: 10,
    C: 100,
    D: 1000,
}

# First element is top, second is bottom.
BOTTOM = 1
TOP = 0
TEST_INPUT1 = [
    [B, A],
    [C, D],
    [B, C],
    [D, A],
]

TEST_INPUT2 = [
    [B, D, D, A],
    [C, C, B, D],
    [B, B, A, C],
    [D, A, C, A],
]

INPUT1 = [
    [A, D],
    [C, D],
    [B, A],
    [B, C],
]

INPUT2 = [
    [A, D, D, D],
    [C, C, B, D],
    [B, B, A, A],
    [B, A, C, C],
]

CORRIDOR_WIDTH = 11
ROOM_SPOTS = [2, 4, 6, 8]

BIG_NUMBER = 10 ** 10


def debug(state: List[Optional[str]], rooms: List[List[Optional[str]]]):
    lines = ["".join(x if x is not None else "." for x in state)]
    for r in range(len(rooms[0])):
        row = []
        for i in range(CORRIDOR_WIDTH):
            if i not in ROOM_SPOTS:
                row.append("#")
                continue

            idx = ROOM_SPOTS.index(i)
            spot = rooms[idx][r]
            row.append(spot if spot is not None else ".")
        lines.append("".join(row))

    print("\n".join(lines))
    print()


def run(data: List[List[str]]) -> int:
    cache = dict()
    state: List[Optional[str]] = [None] * CORRIDOR_WIDTH

    def runner(
        state: List[Optional[str]], rooms: List[List[Optional[str]]]
    ) -> Optional[int]:
        if all(
            all(x is not None and x == ROOM_TO_TYPE[i] for x in room)
            for i, room in enumerate(rooms)
        ):
            return 0

        key = tuple(state), tuple(tuple(room) for room in rooms)
        if key not in cache:
            result = BIG_NUMBER

            # Amphipod can exit a room.
            for i, room in enumerate(rooms):
                room_type = ROOM_TO_TYPE[i]
                j = 0
                while j < len(room) and room[j] is None:
                    j += 1
                if j == len(room):
                    # Room is empty.
                    continue

                if all(x == room_type for x in room[j:]):
                    # Room is finished for now.
                    continue

                to_move = room[j]
                assert to_move is not None
                energy_to_leave = (j + 1) * TYPE_TO_ENERGY[to_move]
                old_room = deepcopy(room)
                room[j] = None

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
                                # Energy to go.
                                + TYPE_TO_ENERGY[to_move] * step
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
                                # Energy to go.
                                + TYPE_TO_ENERGY[to_move] * step
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

                room_idx = ROOM_TO_TYPE.index(x)
                room = rooms[room_idx]

                if any(y is not None and y != x for y in room):
                    # Room has amphipods of a different type.
                    continue

                j = 0
                # Find the last empty spot.
                while j < len(room) and room[j] is None:
                    j += 1

                # Don't need to decrement since we get +1 from the step from the spot into the room.
                effort_to_enter = j * TYPE_TO_ENERGY[x]
                old_room = deepcopy(room)
                room[j - 1] = x

                room_spot = ROOM_SPOTS[room_idx]
                s, e = i + 1, room_spot + 1
                if room_spot < i:
                    s, e = room_spot, i
                if all(y is None for y in state[s:e]):
                    # Path is clear.
                    state[i] = None
                    subresult = runner(state, rooms)
                    state[i] = x
                    if subresult is not None:
                        result = min(
                            result,
                            # Energy to enter the room from its spot.
                            effort_to_enter
                            # Energy to get to the spot.
                            + (e - s) * TYPE_TO_ENERGY[x]
                            # Energy to finish the puzzle.
                            + subresult,
                        )

                rooms[room_idx] = old_room

            if result == BIG_NUMBER:
                # We couldn't do anything.
                result = None
            cache[key] = result

        return cache[key]

    result = runner(state, data)
    assert result is not None
    return result


assrt(12521, run, TEST_INPUT1)


def main():
    res1 = run(INPUT1)
    assert res1 == 18170
    print(run(INPUT2))


if __name__ == "__main__":
    main()
