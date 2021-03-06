from typing import List, NamedTuple, Set, Tuple, Dict
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
import math

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

    def ppp(self):
        print()
        print(self.pp)
        print()

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

    assert(len(outer_tile_ids) == int(math.sqrt(len(tiles))) * 4 - 4)
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
    assert(all(len(vs) == 2 for vs in connections.values()) or len(border_tiles) == 1)
    return connections

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
    connections = connect_border_tiles(corner_tiles, border_tiles)
    if connections != TEST_CONNECTIONS:
        print(f"connect_border_tiles returned {got}, expected {want}")

test_connect_border_tiles()


def recover_border_tiles(start, border_tiles, connections):
    side_size = len(border_tiles) // 4 + 1
    border_tiles = {tile.tile_id: tile for tile in border_tiles}

    def update_tile_to_variant(tile, variant):
        updated = tile.set_to_variant(variant)
        border_tiles[tile.tile_id] = updated
        return updated

    if side_size == 1:
        return [[start]], None

    bottom_tile_id, right_tile_id = connections[start.tile_id]
    right_tile = border_tiles[right_tile_id]
    bottom_tile = border_tiles[bottom_tile_id]

    # Establishing start tile as the top left corner sets all the border tiles in
    # a unique way up to full inversion which is handled later.
    found = False
    for i, (_, sb, sc, _) in enumerate(start.variants):
        if found:
            break
        for j, (_, _, _, rd) in enumerate(right_tile.variants):
            if found:
                break
            for k, (ba, _, _, _) in enumerate(bottom_tile.variants):
                if sb == flip(rd) and flip(sc) == ba:
                    start = update_tile_to_variant(start, i)
                    right_tile = update_tile_to_variant(right_tile, j)
                    bottom_tile = update_tile_to_variant(bottom_tile, k)
                    found = True
                    break

    assert(found)

    def get_connected_tile(tile, avoid):
        for tile_id in connections[tile.tile_id]:
            if tile_id not in avoid:
                return border_tiles[tile_id]

    recovered_tile_ids = [start.tile_id, right_tile.tile_id]
    current = right_tile
    for _ in range(side_size):
        new_tile = get_connected_tile(current, recovered_tile_ids)
        _, b, _, _ = current.desc
        for i, (_, _, _, d) in enumerate(new_tile.variants):
            if b == flip(d):
                current = update_tile_to_variant(new_tile, i)
                recovered_tile_ids.append(current.tile_id)
                break

    assert(len(recovered_tile_ids) == side_size)

    for _ in range(side_size):
        new_tile = get_connected_tile(current, recovered_tile_ids)
        _, _, c, _ = current.desc
        for i, (a, _, _, _) in enumerate(new_tile.variants):
            if c == flip(a):
                current = update_tile_to_variant(new_tile, i)
                recovered_tile_ids.append(current.tile_id)
                break

    assert(len(recovered_tile_ids) == 2 * side_size - 1)

    for _ in range(side_size):
        new_tile = get_connected_tile(current, recovered_tile_ids)
        _, _, _, d = current.desc
        for i, (_, b, _, _) in enumerate(new_tile.variants):
            if d == flip(b):
                current = update_tile_to_variant(new_tile, i)
                recovered_tile_ids.append(current.tile_id)
                break

    assert(len(recovered_tile_ids) == 3 * side_size - 2)

    for _ in range(side_size - 2):
        new_tile = get_connected_tile(current, recovered_tile_ids)
        a, _, _, _ = current.desc
        for i, (_, _, c, _) in enumerate(new_tile.variants):
            if a == flip(c):
                current = update_tile_to_variant(new_tile, i)
                recovered_tile_ids.append(current.tile_id)
                break

    assert(len(recovered_tile_ids) == len(border_tiles))
    assert(recovered_tile_ids[-1] == bottom_tile.tile_id)
    assert(start.desc[2] == flip(bottom_tile.desc[0]))

    recovered_tiles = [border_tiles[i] for i in recovered_tile_ids]
    return postprocess_recovered_tiles(recovered_tiles, side_size)

def postprocess_recovered_tiles(tiles, side_size):
    result = []
    result.append(tiles[:side_size])
    for i in range(1, side_size - 1):
        result.append([])
    result.append(list(reversed(tiles[2 * side_size - 1: 3 * side_size])))
    for i in range(1, side_size - 1):
        result[i].append(tiles[-i])
        result[i].append(tiles[side_size + i])

    return result

def recover_image(tiles):
    border_tiles = get_border_tiles(tiles)
    inner_tiles = [tile for tile in tiles if tile not in border_tiles]
    corner_tiles = get_corner_tiles(border_tiles, inner_tiles)
    connections = connect_border_tiles(corner_tiles, border_tiles)
    recovered_tiles = recover_border_tiles(corner_tiles[0], border_tiles, connections)
    # if len(tiles) < 9:
    #     return recovered_tiles
    inner_tiles = {tile.tile_id: tile for tile in inner_tiles}

    def find_expected_tile(expected_a, expected_d):
        for tile_id, tile in inner_tiles.items():
            for i, (a, _, _, d) in enumerate(tile.variants):
                if expected_a == flip(a) and expected_d == flip(d):
                    tile = tile.set_to_variant(i)
                    del inner_tiles[tile_id]
                    return tile

    expected_a, _, _, _ = recovered_tiles[0][1].desc
    _, _, _, expected_d = recovered_tiles[1][0].desc
    tile = find_expected_tile(expected_a, expected_d)

    if tile is None:
        # It means that the tile is bottom right corner so we should flip the board.
        recovered_tiles = [[tile.horizontal_flip().vertical_flip() for tile in row[::-1]] for row in recovered_tiles[::-1]]

    result = [recovered_tiles[0]]
    side_size = len(recovered_tiles[0])
    for i in range(1, side_size - 1):
        result.append([recovered_tiles[i][0]])
        for j in range(1, side_size - 1):
            expected_a, _, _, _ = result[i - 1][j].desc
            _, _, _, expected_d = result[i][j - 1].desc
            t = find_expected_tile(expected_a, expected_d)
            assert t is not None
            result.append(t)

        result.append([recovered_tiles[i][-1]])

    result.append(recovered_tiles[-1])

    # instead of a recursive call, try recovering the image tile by tile using knowledge of left and upper tile for a given missing tile
    # inner_image = recover_image(inner_tiles, expected_orientation)
    # result = [recovered_tiles[0]]
    # for i, row in enumerate(inner_image):
    #     result.append([recovered_tiles[i + 1][0]] + row + [recovered_tiles[i + 1][-1]])
    # result.append(recovered_tiles[-1])
    return result

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
        image = recover_image(tiles)        



if __name__ == "__main__":
    main()
