import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math




def is_symbol(c: str) -> bool:
    assert len(c) == 1
    return c not in string.digits and c != '.'

aex(False, is_symbol('.'))
aex(True, is_symbol('/'))
aex(False, is_symbol('1'))

def expand_to_number(field: list[str], i: int, l: int, r: int) -> tuple[int, int, int]:
    assert field[i][l] in string.digits
    while l - 1 >= 0 and field[i][l - 1] in string.digits:
        l -= 1

    while r + 1 < len(field[i]) and field[i][r + 1] in string.digits:
        r += 1

    return i, l, r

D = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]

def get_symbols(field: list[str]) -> set[tuple[int, int]]:
    symbols = set()
    for i in range(len(field)):
        for j in range(len(field[i])):
            if is_symbol(field[i][j]):
                symbols.add((i, j))
    return symbols

def get_numbers_from_symbol(field: list[str], i: int, j: int) -> set[tuple[int, int, int]]:
    res = set()
    for dx, dy in D:
        ii = i + dx
        jj = j + dy
        if ii < 0 or ii >= len(field) or jj < 0 or jj >= len(field[i]):
            continue

        if field[ii][jj] in string.digits:
            row, l, r = expand_to_number(field, ii, jj, jj)
            res.add((row, l, r))

    return res

def get_numbers(field: list[str], symbols: set[tuple[int, int]]) -> set[tuple[int, int, int]]:
    numbers = set()

    for i, j in symbols:
        numbers |= get_numbers_from_symbol(field, i, j)

    return numbers

def get_gear_ratios(field: list[str], symbols: set[tuple[int, int]]) -> list[int]:
    result = []

    for i, j in symbols:
        if field[i][j] == '*':
            numbers = get_numbers_from_symbol(field, i, j)
            if len(numbers) == 2:
                result.append(math.prod(int(field[row][l: r + 1]) for row, l, r in numbers))

    return result

def solve1(field: list[str]) -> int:
    symbols = get_symbols(field)
    numbers = get_numbers(field, symbols)
    return sum(int(field[i][l:r+1]) for i, l, r in numbers)

TEST_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

aex(4361, solve1(splitlines(TEST_INPUT)))



def solve2(field: list[str]) -> int:
    symbols = get_symbols(field)
    ratios = get_gear_ratios(field, symbols)
    return sum(ratios)


aex(467835, solve2(splitlines(TEST_INPUT)))

def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))

if __name__ == "__main__":
    main()