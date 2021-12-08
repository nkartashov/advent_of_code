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

# segment count -> digit
SEGMENT_COUNTS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}

def includes(bigger: str, smaller: str) -> bool:
    return set(bigger).issuperset(set(smaller))

assert includes('fbcad', 'dab')
assert not includes('fbcad', 'deb')

def find_missing_segment(digit: str) -> str:
    assert len(digit) == 6
    segments = set('abcdefg')
    for d in digit:
        segments.remove(d)
    assert len(segments) == 1
    return segments.pop()


def decode_line(line: Line) -> int:
    # digit -> code
    known = {}
    for digit in line.digits:
        if len(digit) in SEGMENT_COUNTS:
            known[SEGMENT_COUNTS[len(digit)]] = digit
    assert 1 in known
    assert 4 in known
    assert 7 in known
    assert 8 in known

    for digit in line.digits:
        if len(digit) == 6 and includes(digit, known[4]):
            known[9] = digit
            break
    assert 9 in known

    for digit in line.digits:
        if len(digit) == 6 and includes(digit, known[7]) and digit != known[9]:
            known[0] = digit
            break
    assert 0 in known

    for digit in line.digits:
        if len(digit) == 6 and digit != known[9] and digit != known[0]:
            known[6] = digit
            break
    assert 6 in known

    for digit in line.digits:
        if len(digit) == 5 and includes(digit, known[7]):
            known[3] = digit
            break

    assert 3 in known

    missing_segment_from_9 = find_missing_segment(known[9])

    for digit in line.digits:
        if len(digit) == 5 and missing_segment_from_9 not in digit and digit != known[3]:
            known[5] = digit
            break

    for digit in line.digits:
        if len(digit) == 5 and digit != known[5] and digit != known[3]:
            known[2] = digit
            break
    
    decoding = {code: value for value, code in known.items()}
    assert(len(decoding) == 10)
    decoded = [decoding[c] for c in reversed(line.code)]
    result = 0
    mult = 1
    for value in decoded:
        result += mult * value
        mult *= 10
    return result


TEST_STRING = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
assrt(5353, decode_line, parse_line(TEST_STRING))

def solve_part2(lines: List[Line]) -> int:
    result = 0
    for line in lines:
        result += decode_line(line)
    return result

        

def main():
    with open('in.txt') as infile:
        lines = [parse_line(line.strip()) for line in infile.readlines()]
        print(count_simple_numbers(lines))
        print(solve_part2(lines))


if __name__ == "__main__":
    main()
