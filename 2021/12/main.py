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

def parse_line(line):
    return line.split('-')

def parse_lines(lines):
    return [parse_line(line.strip()) for line in lines]

def is_big_cave(cave):
    return cave.isupper()

START = 'start'
END = 'end'

class VisitTracker:
    def __init__(self, support_second_visit: bool):
        self._visited = defaultdict(int)
        self._support_second_visit = support_second_visit
        self._made_second_visit = False

    def can_visit(self, node):
        return node not in self._visited or is_big_cave(node) \
                or (self._support_second_visit and not self._made_second_visit and node != START)

    def enter(self, node):
        self._visited[node] += 1
        if self._visited[node] == 2 and not is_big_cave(node):
            self._made_second_visit = True

    def exit(self, node):
        if not is_big_cave(node) and self._visited[node] == 2:
            self._made_second_visit = False

        self._visited[node] -= 1
        if self._visited[node] == 0:
            del self._visited[node]

class Path:
    def __init__(self, support_second_visit: bool):
        self._nodes = []
        self._visit_tracker = VisitTracker(support_second_visit=support_second_visit)

    def add(self, node):
        self._nodes.append(node)
        self._visit_tracker.enter(node)

    def can_visit(self, node):
        return self._visit_tracker.can_visit(node)

    def save(self):
        return tuple(self._nodes)

    def pop(self):
        assert self._nodes

        node = self._nodes[-1]
        self._nodes.pop()
        self._visit_tracker.exit(node)

def solve(edge_list, support_second_visit=False) -> int:
    edges = defaultdict(set)
    for s, e in edge_list:
        edges[s].add(e)
        edges[e].add(s)
    edges = dict(edges)

    result = set()
    path = Path(support_second_visit=support_second_visit)
    path.add(START)
    def produce_paths(current: str):
        for neighbour in edges[current]:
            if path.can_visit(neighbour):
                path.add(neighbour)
                if neighbour == END:
                    result.add(path.save())
                else:
                    produce_paths(neighbour)
                path.pop()
    produce_paths(START)

    return len(result)

TEST_DATA1 = parse_lines("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split())
TEST_DATA2 = parse_lines("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split())

def solve1(edges):
    return solve(edges)


assrt(19, solve1, TEST_DATA1)
assrt(226, solve1, TEST_DATA2)

def solve2(edges):
    return solve(edges, support_second_visit=True)

assrt(103, solve2, TEST_DATA1)
assrt(3509, solve2, TEST_DATA2)

def main():
    with open('in.txt') as infile:
        data = parse_lines(infile.readlines())
        print(solve1(data))
        print(solve2(data))


if __name__ == "__main__":
    main()
