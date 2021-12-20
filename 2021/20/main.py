from typing import List, NamedTuple, Set, Tuple, Optional, Dict, Union, Any
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import Error, deepcopy
from itertools import product
from functools import lru_cache
import math
from typing_extensions import ParamSpecArgs
from sortedcontainers import SortedDict
import functools
import operator


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


def parse_enhancer(line: str) -> List[bool]:
    return [(True if x == "#" else False) for x in line]


def parse_image(image: str) -> List[List[bool]]:
    return [
        [(True if x == "#" else False) for x in line.strip()]
        for line in image.split("\n")
    ]


def read_input():
    enhancer = None
    image = []
    with open("in.txt") as infile:
        enhancer = parse_enhancer(infile.readline().strip())
        infile.readline()
        image = [
            [(True if x == "#" else False) for x in line.strip()]
            for line in infile.readlines()
        ]
    return enhancer, image


DELTAS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


def reconstruct_image(new_image, minx, maxx, miny, maxy) -> List[List[bool]]:
    result = []
    for i in range(minx, maxx):
        result.append([])
        for j in range(miny, maxy):
            result[-1].append(new_image[(i, j)])
    return result


def print_image(image: List[List[bool]]):
    print("\n".join("".join("#" if x else "." for x in row) for row in image))
    print()


def square_all_set(new_image, i, j):
    return all(new_image[(i + dx, j + dy)] for dx, dy in DELTAS)


def should_early_exit(new_image, minx, maxx, miny, maxy) -> bool:
    for i in range(minx + 1, maxx - 1):
        for j in [miny + 1, maxy - 2]:
            if not square_all_set(new_image, i, j):
                return False

    for j in range(miny + 1, maxy - 1):
        for i in [minx + 1, maxx - 2]:
            if not square_all_set(new_image, i, j):
                return False

    return True


def enhance(
    enhancer: List[bool], image: List[List[bool]], early_exit=False
) -> List[List[bool]]:
    def getter(i, j) -> bool:
        if not (0 <= i < len(image) and 0 <= j < len(image[0])):
            return False
        return image[i][j]

    def get_pixel(i, j) -> bool:
        enhancer_idx = int(
            "".join("1" if getter(i + dx, j + dy) else "0" for dx, dy in DELTAS), base=2
        )
        assert 0 <= enhancer_idx < len(enhancer)
        return enhancer[enhancer_idx]

    new_image = {}
    minx = 0
    maxx = len(image)
    miny = 0
    maxy = len(image[0])
    has_bright_pixel_on_the_edge = False

    for i in range(minx, maxx):
        for j in range(miny, maxy):
            on_the_edge = i in (minx, maxx - 1) or j in (miny, maxy - 1)
            new_image[(i, j)] = get_pixel(i, j)
            has_bright_pixel_on_the_edge = has_bright_pixel_on_the_edge or (
                on_the_edge and new_image[(i, j)]
            )

    while has_bright_pixel_on_the_edge and not (
        early_exit and should_early_exit(new_image, minx, maxx, miny, maxy)
    ):
        has_bright_pixel_on_the_edge = False
        minx -= 1
        maxx += 1
        miny -= 1
        maxy += 1

        for i in range(minx, maxx):
            for j in [miny, maxy - 1]:
                new_image[(i, j)] = get_pixel(i, j)
                has_bright_pixel_on_the_edge = (
                    has_bright_pixel_on_the_edge or new_image[(i, j)]
                )

        for j in range(miny, maxy):
            for i in [minx, maxx - 1]:
                new_image[(i, j)] = get_pixel(i, j)
                has_bright_pixel_on_the_edge = (
                    has_bright_pixel_on_the_edge or new_image[(i, j)]
                )

    return reconstruct_image(new_image, minx, maxx, miny, maxy)


def solve1(
    enhancer: List[bool], image: List[List[bool]], times=2, is_test=False
) -> int:
    while times:
        print(f"Enhancing {times}")
        times -= 1
        image = enhance(enhancer, image, early_exit=True)
        if not is_test and times % 2 == 0:
            image = [row[6:-6] for row in image[6:-6]]

    return sum(sum(1 if i else 0 for i in row) for row in image)


TEST_IMAGE = parse_image(
    """#..#.
#....
##..#
..#..
..###"""
)

TEST_ENHANCER = parse_enhancer(
    "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
)

assrt(35, solve1, TEST_ENHANCER, TEST_IMAGE, 2, True)


def solve2(
    enhancer: List[bool], image: List[List[bool]], times=50, is_test=False
) -> int:
    return solve1(enhancer, image, times=times, is_test=is_test)


assrt(3351, solve2, TEST_ENHANCER, TEST_IMAGE, 50, True)


def main():
    data = read_input()
    print(solve1(*data))
    print(solve2(*data))


if __name__ == "__main__":
    main()
