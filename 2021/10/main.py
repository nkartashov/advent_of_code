from typing import List, NamedTuple, Set, Tuple, Optional
from enum import Enum
from collections import defaultdict, deque
from copy import deepcopy
from itertools import product
from functools import lru_cache
import math

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

CLOSING_BRACKETS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

OPENING_BRACKETS = {v: k for k, v in CLOSING_BRACKETS.items()}

def find_first_incorrect_index(line: str) -> Optional[int]:
    brackets = []
    for i, ch in enumerate(line):
        if ch not in CLOSING_BRACKETS:
            brackets.append(ch)
            continue
        if not brackets or CLOSING_BRACKETS[ch] != brackets[-1]:
            return i
        else:
            brackets.pop()
    return None

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def solve1(data: List[str]) -> int:
    result = 0
    for line in data:
        index = find_first_incorrect_index(line)
        if index is not None:
            value = SCORES.get(line[index])
            assert value is not None
            result += value
    return result

TEST_DATA = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split()

assrt(26397, solve1, TEST_DATA)

def complete_line(line: str) -> str:
    brackets = []
    for i, ch in enumerate(line):
        if ch not in CLOSING_BRACKETS:
            brackets.append(ch)
            continue
        assert brackets and CLOSING_BRACKETS[ch] == brackets[-1]
        brackets.pop()

    return ''.join(OPENING_BRACKETS[ch] for ch in reversed(brackets))

assrt('}}]])})]', complete_line, '[({(<(())[]>[[{[]{<()<>>')
assrt('}}>}>))))', complete_line, '(((({<>}<{<{<>}{[]{[]{}')


COMPLETE_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def score_completed_line(line: str) -> int:
    result = 0
    for ch in line:
        result = result * 5 + COMPLETE_SCORES[ch]
    return result

assrt(288957, score_completed_line, '}}]])})]')
assrt(5566, score_completed_line, ')}>]})')
assrt(1480781, score_completed_line, '}}>}>))))')
assrt(995444, score_completed_line, ']]}}]}]}>')
assrt(294, score_completed_line, '])}>')


def solve2(data: List[str]) -> int:
    completed_scores = []
    for line in data:
        if find_first_incorrect_index(line) is None:
            completed_scores.append(score_completed_line(complete_line(line)))
    completed_scores.sort()
    return completed_scores[len(completed_scores) // 2]

assrt(288957, solve2, TEST_DATA)


def main():
    with open('in.txt') as infile:
        data = [line.strip() for line in infile.readlines()]
        print(solve1(data))
        print(solve2(data))


if __name__ == "__main__":
    main()
