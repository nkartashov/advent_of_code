from typing import List, NamedTuple, Set, Tuple, Optional, Dict
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import deepcopy
from itertools import product
from functools import lru_cache
import math
from sortedcontainers import SortedDict


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def parse_field(lines, mult=1):
    return Field([[int(x) for x in line.strip()] for line in lines], mult)


D_CELL2 = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def get_neighbours(cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = cell
    return [(x + dx, y + dy) for dx, dy in D_CELL2]


DIST_MAX = 10 ** 10
START = (0, 0)


class Field:
    def __init__(self, field, mult):
        self._field = field
        self._mult = mult

    @property
    def lenx(self):
        return len(self._field) * self._mult

    @property
    def leny(self):
        return len(self._field[0]) * self._mult

    def get(self, x, y):
        wrap = x // len(self._field)
        wrap += y // len(self._field[0])
        x = x % len(self._field)
        y = y % len(self._field[0])
        res = self._field[x][y]
        while wrap:
            res += 1
            if res > 9:
                res = 1
            wrap -= 1
        return res


def solve1(field):
    END = (field.lenx - 1, field.leny - 1)
    dist: Dict[Tuple[int, int], int] = {START: 0}
    to_visit = SortedDict({0: set([START])})
    while to_visit:
        cur_dist, nodes = to_visit.peekitem(0)
        assert nodes

        node = nodes.pop()
        if not nodes:
            del to_visit[cur_dist]

        if node == END:
            break
        for neighbour in get_neighbours(node):
            nx, ny = neighbour
            if 0 <= nx < field.lenx and 0 <= ny < field.leny:
                cur_neigh_dist: int = dist.get(neighbour, DIST_MAX)
                new_neigh_dist = cur_dist + field.get(nx, ny)
                if new_neigh_dist < cur_neigh_dist:
                    dist[neighbour] = new_neigh_dist

                    # Remove from old collection.
                    cur_neigh_col = to_visit.get(cur_neigh_dist, set())
                    if neighbour in cur_neigh_col:
                        cur_neigh_col.remove(neighbour)
                        if not cur_neigh_col:
                            del to_visit[cur_neigh_dist]

                    # Add to the new one.
                    new_neigh_col = to_visit.get(new_neigh_dist)
                    if new_neigh_col is None:
                        to_visit[new_neigh_dist] = set()
                        new_neigh_col = to_visit[new_neigh_dist]
                    new_neigh_col.add(neighbour)

    return dist[END]


TEST_DATA1 = parse_field(
    """11
13
21""".split(
        "\n"
    )
)

TEST_DATA2 = parse_field(
    """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split(
        "\n"
    )
)

TEST_DATA3 = parse_field(
    """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split(
        "\n"
    ),
    mult=5,
)

assrt(4, solve1, TEST_DATA1)
assrt(40, solve1, TEST_DATA2)
assrt(315, solve1, TEST_DATA3)


def main():
    with open("in.txt") as infile:
        lines = infile.readlines()
        field = parse_field(lines)
        print(solve1(field))
        print(solve1(parse_field(lines, mult=5)))


if __name__ == "__main__":
    main()
