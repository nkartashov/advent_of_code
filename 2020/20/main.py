from typing import List, NamedTuple, Set, Tuple, Dict
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product

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
        (flip(c), flip(b), flip(a), flip(d)), # horizontal flip
        (flip(a), flip(d), flip(c), flip(b)), # vertical flip
        (flip(d), flip(c), flip(b), flip(a)), # rotate -> horizontal flip 
        (flip(b), flip(a), flip(d), flip(c)), # rotate -> vertical flip
    ]

class Tile(NamedTuple):
    tile_id: int
    data: List[str]

    @property
    def desc(self):
        return tuple(to_binary(code) for code in (
            self.data[0],
            (row[-1] for row in self.data),
            reversed(self.data[-1]),
            reversed([row[0] for row in self.data]),
        ))

    @property
    def variants(self):
        return generate_variants(self.desc)

    @property
    def pp(self):
        return '\n'.join(self.data)

    def rotate(self):
        return Tile(self.tile_id, [''.join(row) for row in zip(*self.data)][::-1])

    def horizontal_flip(self):
        return Tile(self.tile_id, self.data[::-1])

    def vertical_flip(self):
        return Tile(self.tile_id, [row[::-1] for row in self.data])

    def set_to_variant(self, variant_idx):
        # See generate variants
        result = self
        if variant_idx < 4:
            while variant_idx > 0:
                variant_idx -= 1
                result = result.rotate()
            return result

        if variant_idx >= 6:
            result = result.rotate()

        if variant_idx % 2 == 0:
            return result.horizontal_flip()
        return result.vertical_flip()


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
    for tile in tiles:
        for desc in generate_variants(tile.desc):
            a, b, c, d = desc
            horizontal_set[a].append(tile.tile_id)
            horizontal_set[c].append(tile.tile_id)
    outer_tile_ids = set_sum([set(ms) for d, ms in horizontal_set.items() if len(ms) == 2])
    return [tile for tile in tiles if tile.tile_id in outer_tile_ids]

def read_test_tiles():
    with open('test_tiles.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        return read_tiles(lines)

TEST_TILES = read_test_tiles()
TEST_OUTER_TILE_IDS = {1951, 2311, 3079, 2473, 1171, 1489, 2971, 2729}

def test_set_variant():
    tile = TEST_TILES[0]
    for i, expected in enumerate(tile.variants):
        actual = tile.set_to_variant(i).desc
        if actual != expected:
            print(f"set_to_variant returned {actual} for variant {i}, expected {expected}")
        
test_set_variant()

def test_get_border_tiles():
    actual = {tile.tile_id for tile in get_border_tiles(TEST_TILES)}
    if actual != TEST_OUTER_TILE_IDS:
        print(f"get_border_tiles returned {got}, expected {want}")

test_get_border_tiles()

def get_corner_tiles(border_tiles, inner_tiles):
    # Corner tiles don't have any edges coming into them from non-border tiles.
    border_tiles = {tile.tile_id: tile for tile in border_tiles}
    corner_tiles = deepcopy(border_tiles)
    available_edges = dict()
    for tile in border_tiles.values():
        for desc in generate_variants(tile.desc):
            for edge in desc:
                available_edges[edge] = tile

    for tile in inner_tiles:
        for desc in generate_variants(tile.desc):
            for edge in desc:
                if edge in available_edges:
                    not_corner_tile_id = available_edges[edge].tile_id
                    if not_corner_tile_id in corner_tiles:
                        del corner_tiles[not_corner_tile_id]

    return list(corner_tiles.values())

def connect_border_tiles(corner_tiles, border_tiles):
    top_left_tile = corner_tiles[0]
    # We're gonna iteratively try to find any tile which is connected to the current set via edges.
    last_added = top_left_tile
    connections = defaultdict(set)
    connections[top_left_tile.tile_id] = set()

    def connect_tiles(id1, id2):
        connections[id1].add(id2)
        connections[id2].add(id1)

    while True:
        rest_border_tiles = [tile for tile in border_tiles if tile.tile_id not in connections]
        found = False

        for tile in rest_border_tiles:
            if found:
                break
            for variant in generate_variants(tile.desc):
                if found:
                    break
                for edge in variant:
                    if edge in last_added.desc:
                        parent_id = last_added.tile_id
                        connect_tiles(parent_id, tile.tile_id)
                        last_added = tile
                        found = True
                        break
        if not found:
            break

    connect_tiles(top_left_tile.tile_id, last_added.tile_id)
    return top_left_tile, connections

TEST_CONNECTIONS = {
    1951: {2311, 2729},
    2311: {1951, 3079},
    3079: {2311, 2473},
    2473: {3079, 1171},
    1171: {2473, 1489},
    1489: {1171, 2971},
    2971: {1489, 2729},
    2729: {2971, 1951},
}

def test_connect_border_tiles():
    border_tiles = get_border_tiles(TEST_TILES)
    inner_tiles = [tile for tile in TEST_TILES if tile not in border_tiles]
    corner_tiles = get_corner_tiles(border_tiles, inner_tiles)
    start, connections = connect_border_tiles(corner_tiles, border_tiles)
    if connections != TEST_CONNECTIONS:
        print(f"connect_border_tiles returned {got}, expected {want}")

test_connect_border_tiles()

def recover_border_tiles(start, border_tiles, corner_tiles, inner_tiles, connections):
    side_size = len(connections) / 4 + 1
    border_tiles = {tile.tile_id: tile for tile in border_tiles}
    right_tile_id, bottom_tile_id = connections[start.tile_id]
    right_tile = border_tiles[right_tile_id]
    bottom_tile = border_tiles[bottom_tile_id]

    def update_tile_to_variant(tile, variant):
        border_tiles[tile.tile_id] = tile.set_to_variant(variant)

    # Establishing start tile as the top left corner sets all the border tiles in
    # a unique way up to full inversion which is handled later.
    found = False
    for i, (sa, sb, sc, sd) in enumerate(start.variants):
        if found:
            break
        for j, (ra, rb, rc, rd) in enumerate(right_tile.variants):
            if found:
                break
            for k, (ba, bb, bc, bd) in enumerate(bottom_tile.variants):
                if sb == flip(rd) and flip(sc) == ba:
                    update_tile_to_variant(start, i)
                    update_tile_to_variant(right_tile, j)
                    update_tile_to_variant(bottom_tile, k)
                    found = True
                    break


def get_answer(corner_tiles):
    result = 1
    for tile in corner_tiles:
        result *= tile.tile_id
    return result

def main():
    lines = None
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        tiles = read_tiles(lines)
        border_tiles = get_border_tiles(tiles)
        inner_tiles = [tile for tile in tiles if tile not in border_tiles]
        corner_tiles = get_corner_tiles(border_tiles, inner_tiles)
        print(get_answer(corner_tiles))
        start, connections = connect_border_tiles(corner_tiles, border_tiles)
        recover_border_tiles(start, border_tiles, corner_tiles, inner_tiles, connections)



if __name__ == "__main__":
    main()
