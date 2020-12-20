from typing import List, NamedTuple, Set, Tuple, Dict
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

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
        return 0
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
            reversed(row[0] for row in self.data),
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


def main():
    lines = None
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        tiles = read_tiles(lines)
        print(len(tiles))
        result = set()
        for tile in tiles:
            pass



if __name__ == "__main__":
    main()
