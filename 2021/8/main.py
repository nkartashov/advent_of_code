from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class Line(NamedTuple):
    digits: List[str]
    code: List[str]

    def __repr__(self):
        return f"{' '.join(self.digits)} | {' '.join(self.code)}"

def parse_line(line):
    digits_str, code_str = [part.strip() for part in line.split('|')]
    return Line(
            digits=[''.join(sorted(s)) for s in digits_str.split()],
            code=[''.join(sorted(s)) for s in code_str.split()])

def count_simple_numbers(lines: List[Line]) -> int:
    result = 0
    for line in lines:
        for s in line.code:
            if len(s) in {2, 4, 3, 7}:
                result += 1
    return result

TEST_STRING = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'

def main():
    with open('in.txt') as infile:
        lines = [parse_line(line.strip()) for line in infile.readlines()]
        print(count_simple_numbers(lines))


if __name__ == "__main__":
    main()
