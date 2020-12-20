from typing import List, NamedTuple, Set, Tuple, Dict
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache
import random as rnd

rnd.seed(42)

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def set_sum(args):
    result = set()
    for arg in args:
        result = result | arg
    return result

def to_binary(code):
    def mapper(x):
        if x == '#':
            return '1'
        return '0'
    return int(''.join(mapper(x) for x in code), 2)

def flip(code):
    return int('{:010b}'.format(code)[::-1], 2)

assrt(int('1110111011', 2), flip, int('1101110111', 2))

def generate_variants(descriptor):
    a, b, c, d = descriptor

    return [
        (a, b, c, d),
        (b, c, d, a),
        (c, d, a, b),
        (d, a, b, c),
        (flip(c), flip(b), flip(a), flip(d)),
        (flip(a), flip(d), flip(c), flip(b)),
        (flip(d), flip(c), flip(b), flip(a)),
        (flip(b), flip(a), flip(d), flip(c)),
    ]
    pass

class Tile(NamedTuple):
    tile_id: int
    data: List[str]

    @property
    def desc(self):
        return (to_binary(code) for code in (
            self.data[0],
            (row[-1] for row in self.data),
            reversed([row[0] for row in self.data]),
            reversed(self.data[-1]),
        ))


def read_tiles(lines):
    i = 0
    result = []
    while i < len(lines):
        # Tile <number>:
        # 10 lines
        # line feed
        _, tile_id_string = lines[i][:-1].split()
        result.append(Tile(tile_id=int(tile_id_string), data=lines[i + 1: i + 11]))
        i += 12

    return result


def get_border_tiles(tiles):
    horizontal_set = defaultdict(list)
    for i, tile in enumerate(tiles):
        for desc in generate_variants(tile.desc):
            a, b, c, d = desc
            horizontal_set[a].append(i)
            horizontal_set[c].append(i)

    outer_tile_idxs = set_sum([set(ms) for d, ms in horizontal_set.items() if len(ms) == 2])
    return [tiles[idx] for idx in outer_tile_idxs]

def read_test_tiles():
    with open('test_tiles.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        return read_tiles(lines)

TEST_TILES = read_test_tiles()
TEST_OUTER_TILE_IDS = {1951, 2311, 3079, 2473, 1171, 1489, 2971, 2729}

def test_get_border_tiles():
    actual = {tile.tile_id for tile in get_border_tiles(TEST_TILES)}
    if actual != TEST_OUTER_TILE_IDS:
        print(f"get_border_tiles returned {got}, expected {want}")

test_get_border_tiles()

def find_corner_tiles(border_tiles):
    
    pass
	

def main():
    lines = None
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        tiles = read_tiles(lines)
        border_tiles = get_border_tiles(tiles)



if __name__ == "__main__":
    main()
