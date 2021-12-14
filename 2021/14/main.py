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

    @property
    def new_pairs(self):
        return [self.pair[0] + self.insert, self.insert + self.pair[1]]

def parse_data(data):
    polymer = data[0]
    rules = []
    for line in data[2:]:
        left, right = line.split('->')
        rules.append(Rule(pair=left.strip(), insert=right.strip()))
    return polymer, rules

DEFAULT_CHUNK_SIZE = 10
CHUNK_SIZES = [
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_SIZE * 10,
    DEFAULT_CHUNK_SIZE * 100,
]

def simulate_polymerisation(polymer: str, rules: List[Rule], steps: int) -> str:
    def run_explicit_step(pol):
        assert len(pol) <= DEFAULT_CHUNK_SIZE

        new_pol = [pol[0]]
        for i in range(1, len(pol)):
            pattern = pol[i - 1: i + 1] 
            for rule in rules:
                if pattern == rule.pair:
                    new_pol.append(rule.insert)
                    break
            new_pol.append(pol[i])
        return ''.join(new_pol)

    def run_cached_step(pol, cache, chunk_size_idx):
        chunk_size = CHUNK_SIZES[chunk_size_idx]
        new_pol = []
        start = 0
        while start < len(pol):
            chunk = pol[start: start + chunk_size]
            if chunk not in chunk_cache:
                if chunk_size_idx == 0:
                    chunk_cache[chunk] = run_explicit_step(chunk)
                else:
                    chunk_cache[chunk] = run_cached_step(chunk, cache, chunk_size_idx - 1)

            new_chunk = chunk_cache[chunk]
            if start > 0:
                # find a rule which connects the two
                pattern = pol[start - 1: start + 1]
                for rule in rules:
                    if pattern == rule.pair:
                        new_pol.append(rule.insert)
                        break
            new_pol.append(new_chunk)
            start += chunk_size

        result = ''.join(new_pol)
        return result

    chunk_cache = {}
    for step in range(steps):
        polymer = run_cached_step(polymer, chunk_cache, len(CHUNK_SIZES) - 1)

    return polymer


def simulate_polymerisation_with_counts(polymer: str, rules: List[Rule], steps: int) -> str:
    cache = {}
    def run_pair(pair, depth):
        if depth == 0:
            return Counter()

        key = (pair, depth)
        if key not in cache:
            cache[key] = Counter()
            for rule in rules:
                if rule.pair == pair:
                    cache[key] = Counter(rule.insert) + sum((run_pair(p, depth - 1) for p in rule.new_pairs), Counter())
                    
        return cache[key]

    result = Counter()
    for i in range(1, len(polymer)):
        result += run_pair(polymer[i - 1: i + 1], steps) 
    return result + Counter(polymer)

def solve(polymer: str, rules: List[Rule], steps) -> int:
    result = simulate_polymerisation(polymer, rules, steps)
    counts = Counter(result)
    return counts.most_common(1)[0][1] - counts.most_common(len(counts))[-1][1]

def solve_with_counts(polymer: str, rules: List[Rule], steps) -> int:
    counts = simulate_polymerisation_with_counts(polymer, rules, steps)
    return counts.most_common(1)[0][1] - counts.most_common(len(counts))[-1][1]

def solve1(polymer: str, rules: List[Rule]) -> int:
    return solve_with_counts(polymer, rules, 10)

def solve2(polymer: str, rules: List[Rule]) -> int:
    return solve_with_counts(polymer, rules, 40)

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

assrt(Counter("NCNBCHB"), simulate_polymerisation_with_counts, TEST_POL, TEST_RULES, 1)
assrt(Counter("NBCCNBBBCBHCB"), simulate_polymerisation_with_counts, TEST_POL, TEST_RULES, 2)
assrt(Counter("NBBBCNCCNBBNBNBBCHBHHBCHB"), simulate_polymerisation_with_counts, TEST_POL, TEST_RULES, 3)
assrt(Counter("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"), simulate_polymerisation_with_counts, TEST_POL, TEST_RULES, 4)

assrt(2188189693529, solve2, TEST_POL, TEST_RULES)


def main():
    with open('in.txt') as infile:
        data = parse_data([line.strip() for line in infile.readlines()])
        print(solve1(*data))
        assert solve1(*data) == 2194
        print(solve2(*data))


if __name__ == "__main__":
    main()
