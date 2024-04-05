import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math
from typing import Optional
from collections import Counter
import re


class Node(BaseModel):
    label: str
    left: str
    right: str


class Input(BaseModel):
    instructions: str
    nodes: dict[str, Node]


def parse_input(lines: list[str]) -> Input:
    instructions = lines[0]
    nodes = []
    for line in lines[2:]:
        match = re.match(r"(\w+) \= \((\w+), (\w+)\)", line)
        assert match is not None
        label, left, right = match.groups()
        nodes.append(Node(label=label, left=left, right=right))

    return Input(instructions=instructions, nodes={node.label: node for node in nodes})


def solve1(lines: list[str]) -> int:
    inp = parse_input(lines)
    i = 0
    current = inp.nodes["AAA"]
    step = 0
    while current.label != "ZZZ":
        step += 1
        move = inp.instructions[i]
        if move == "L":
            current = inp.nodes[current.left]
        else:
            current = inp.nodes[current.right]
        i = (i + 1) % len(inp.instructions)

    return step


TEST_INPUT = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

aex(6, solve1(splitlines(TEST_INPUT)))


def _find_cycle(current: Node, inp: Input) -> int:
    i = 0
    step = 0
    seen = set()
    while (current.label, i) not in seen:
        seen.add((current.label, i))
        step += 1
        move = inp.instructions[i]
        if move == "L":
            current = inp.nodes[current.left]
        else:
            current = inp.nodes[current.right]
        i = (i + 1) % len(inp.instructions)
        if current.label.endswith("Z"):
            return step

    raise ValueError("No cycle found")


def solve2(lines: list[str]) -> int:
    inp = parse_input(lines)
    start_nodes = [node for node in inp.nodes.values() if node.label.endswith("A")]
    return math.lcm(*[_find_cycle(node, inp) for node in start_nodes])


TEST_INPUT2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

aex(6, solve2(splitlines(TEST_INPUT2)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))


if __name__ == "__main__":
    main()
