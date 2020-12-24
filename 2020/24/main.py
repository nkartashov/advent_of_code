from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache
from tqdm import tqdm

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def set_sum(args):
    result = set()
    for arg in args:
        result = result | arg
    return result

class Direction(Enum):
    E = 'e'
    SE = 'se'
    SW = 'sw'
    W = 'w'
    NE = 'ne'
    NW = 'nw'


def tokenize_input(line):
    result = []
    i = 0
    while i < len(line):
        for direction in Direction:
            if line.startswith(direction.value, i):
                result.append(direction)
                i += len(direction.value)
    return result

TEST_DIRECTIONS = [Direction.NW, Direction.W, Direction.SW, Direction.E, Direction.E]
assrt(TEST_DIRECTIONS, tokenize_input, 'nwwswee')

def to_canonical_form(x, y1, y2):
    sign = 1 
    if x > 0:
        sign = x // abs(x)
    return 0, y1 + sign * x, y2 - sign * x

def process_directions(directions):
    x, y1, y2 = 0, 0, 0
    for direction in directions:
        if direction == Direction.E:
            x += 1
        if direction == Direction.SE:
            y1 += 1
        if direction == Direction.SW:
            y2 += 1
        if direction == Direction.W:
            x -= 1
        if direction == Direction.NW:
            y1 -= 1
        if direction == Direction.NE:
            y2 -= 1

    return to_canonical_form(x, y1, y2)

assrt((0, 0, 0), process_directions, TEST_DIRECTIONS)

def get_flipped(lines):
    flipped = set()
    for line in lines:
        position = process_directions(tokenize_input(line))
        if position in flipped:
            flipped.remove(position)
        else:
            flipped.add(position)
    return flipped

def part1(lines):
    return len(get_flipped(lines))

TEST_LINES = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split()

assrt(10, part1, TEST_LINES)

D_CELL = [
    (0, 0, 1),
    (0, 0, -1),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
]

def get_neighbours(x, y1, y2):
    return [to_canonical_form(x + dx, dy1 + dy1, y2 + dy2) for dx, dy1, dy2 in D_CELL]

def simulate_cycle(active_set):
    flipped_count = defaultdict(int)
    for cell in active_set:
        for neighbour in get_neighbours(*cell):
            flipped_count[neighbour] += 1

    def is_flipped(cell):
        count = flipped_count[cell]
        if count == 2:
            return True
        return cell in active_set and count == 1
    
    return {cell for cell in flipped_count if is_flipped(cell)}

def part2(lines):
    flipped = get_flipped(lines)
    for _ in range(100):
        print(len(flipped))
        flipped = simulate_cycle(flipped)
    return len(flipped)

assrt(2208, part2, TEST_LINES)


def read_input(filename='in.txt'):
    with open(filename) as infile:
        return [line.strip() for line in infile.readlines()]

def main():
    input_data = read_input()
    print(part1(input_data))


if __name__ == "__main__":
    main()
