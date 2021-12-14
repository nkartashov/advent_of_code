from typing import List, NamedTuple, Set, Tuple, Optional
from enum import Enum
from collections import defaultdict, deque, Counter
from copy import deepcopy
from itertools import product
from functools import lru_cache
import math

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class Rule(NamedTuple):
    pair: str
    insert: str

def parse_data(data):
    polymer = data[0]
    rules = []
    for line in data[2:]:
        left, right = line.split('->')
        rules.append(Rule(pair=left.strip(), insert=right.strip()))
    return polymer, rules

def simulate_polymerisation(polymer: str, rules: List[Rule], steps: int = 10) -> str:
    while steps != 0:
        print(f"Step {steps}")
        new_polymer = [polymer[0]]
        for i in range(1, len(polymer)):
            for rule in rules:
                if polymer[i - 1: i - 1 + len(rule.pair)] == rule.pair:
                    new_polymer.append(rule.insert)
            new_polymer.append(polymer[i])
        polymer = ''.join(new_polymer)
        steps -= 1
    return polymer

def solve(polymer: str, rules: List[Rule], steps=10) -> int:
    result = simulate_polymerisation(polymer, rules, steps)
    counts = Counter(result)
    return counts.most_common(1)[0][1] - counts.most_common(len(counts))[-1][1]

def solve1(polymer: str, rules: List[Rule]) -> int:
    return solve(polymer, rules, 10)

def solve2(polymer: str, rules: List[Rule]) -> int:
    return solve(polymer, rules, 40)

TEST_POL, TEST_RULES = parse_data("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split('\n'))

assrt("NCNBCHB", simulate_polymerisation, TEST_POL, TEST_RULES, 1)
assrt("NBCCNBBBCBHCB", simulate_polymerisation, TEST_POL, TEST_RULES, 2)
assrt("NBBBCNCCNBBNBNBBCHBHHBCHB", simulate_polymerisation, TEST_POL, TEST_RULES, 3)
assrt("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB", simulate_polymerisation, TEST_POL, TEST_RULES, 4)




def main():
    with open('in.txt') as infile:
        data = parse_data([line.strip() for line in infile.readlines()])
        print(solve1(*data))
        print(solve2(*data))


if __name__ == "__main__":
    main()
