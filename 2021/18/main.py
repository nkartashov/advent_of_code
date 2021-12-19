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


class Node:
    def __init__(self, *, value: Optional[int], parent: Optional["Node"]):
        self._left = None
        self._right = None
        self._value = value
        self._parent = parent

    def set_left(self, left):
        if left is not None:
            left._parent = self
        self._left = left

    def set_right(self, right):
        if right is not None:
            right._parent = self
        self._right = right

    def set_value(self, value):
        self._value = value

    def magnitude(self):
        if self._value is not None:
            return self._value

        return 3 * self._left.magnitude() + 2 * self._right.magnitude()

    def is_nested4(self):
        depth = 0
        parent = self._parent
        while parent is not None:
            parent = parent._parent
            depth += 1

        return depth >= 4

    def is_number(self) -> bool:
        result = self._value is not None
        if result:
            assert self._left is None
            assert self._right is None
        return result

    def is_pair(self) -> bool:
        result = self._value is None
        if result:
            assert self._left is not None
            assert self._right is not None
        return result

    def is_terminal_pair(self) -> bool:
        return self.is_pair() and self._left.is_number() and self._right.is_number()

    def explode(self) -> bool:
        if not (self._value is None and self.is_nested4()):
            return False

        assert self.is_terminal_pair()

        prev_node = self.previous_node()
        if prev_node is not None:
            prev_node._value += self._left._value

        next_node = self.next_node()
        if next_node is not None:
            next_node._value += self._right._value

        self.set_left(None)
        self.set_right(None)
        self.set_value(0)
        return True

    def split(self):
        if not (self._value is not None and self._value >= 10):
            return False

        left_value = self._value // 2
        right_value = self._value - left_value
        self._value = None
        self.set_left(Node(value=left_value, parent=self))
        self.set_right(Node(value=right_value, parent=self))
        return True

    def copy(self):
        if self.is_number():
            result = Node(value=self._value, parent=None)
            return result

        result = Node(value=None, parent=None)
        result.set_left(self._left.copy())
        result.set_right(self._right.copy())
        return result

    def __add__(self, other: "Node") -> "Node":
        result = Node(value=None, parent=None)
        result.set_left(self.copy())
        result.set_right(other.copy())
        result.reduce()
        return result

    def reduce(self):
        def run_explode(node: "Node", depth=0):
            if node.is_pair():
                if run_explode(node._left, depth + 1):
                    return True

                if run_explode(node._right, depth + 1):
                    return True

                if depth >= 4 and node.is_terminal_pair():
                    return node.explode()
            return False

        def run_split(node):
            if node.is_number():
                if node._value >= 10:
                    return node.split()
            else:
                if run_split(node._left):
                    return True

                return run_split(node._right)
            return False

        reduction_happened = True
        while reduction_happened:
            # print(f"Before: {self}")
            reduction_happened = run_explode(self)
            # print(f"After explode {reduction_happened}: {self}")
            if not reduction_happened:
                reduction_happened = run_split(self)
                # print(f"After split {reduction_happened}: {self}")

        return self

    def previous_node(self):
        parent = self._parent
        node = self
        while True:
            if parent is None:
                return None

            # We came from the right node, so get the rightmost child of the left node.
            if node.exeq(parent._right):
                node = parent._left
                while node._right is not None:
                    node = node._right
                return node

            # We came from the left node, so go up until we come from the right or run out of nodes
            node = parent
            parent = parent._parent

    def next_node(self):
        parent = self._parent
        node = self
        while True:
            if parent is None:
                return None

            # We came from the left node, so get the leftmost child of the right node.
            if node.exeq(parent._left):
                node = parent._right
                while node._left is not None:
                    node = node._left
                return node

            # We came from the right node, so go up until we come from the left or run out of nodes
            node = parent
            parent = parent._parent

    def __eq__(self, other):
        return (
            # Exactly the same.
            self.exeq(other)
            # Or structurally equal.
            or isinstance(other, Node)
            and (
                self.is_number()
                and self._value == other._value
                or self._left == other._left
                and self._right == other._right
            )
        )

    def exeq(self, other):
        return id(self) == id(other)

    def __repr__(self):
        if self._value is not None:
            return f"{self._value}"

        assert self._left is not None
        assert self._right is not None
        return f"[{self._left}, {self._right}]"


def parse_node(data, parent=None) -> Node:
    if isinstance(data, int):
        return Node(value=data, parent=parent)

    assert isinstance(data, List)

    parent = Node(value=None, parent=parent)
    parent.set_left(parse_node(data[0], parent=parent))
    parent.set_right(parse_node(data[1], parent=parent))
    return parent


assert parse_node([[[[[9, 8], 1], 2], 3], 4])._left._left._left._left.is_nested4()
assert not parse_node([[[[[9, 8], 1], 2], 3], 4])._left._left._left.is_nested4()

assert parse_node([4, [3, 2]])._right.previous_node()._value == 4
assert parse_node([[4, 5], [6, 7]])._right.previous_node()._value == 5


def previous_node_example1():
    node = parse_node(
        [
            [
                [[[7, 7], [7, 8]], [[9, 5], [8, 7]]],
                [[[6, 8], [0, 8]], [[9, 9], [9, 0]]],
            ],
            [[2, [2, 2]], [8, [8, 1]]],
        ]
    )
    assert node._left._left._left._left == parse_node([7, 7])
    aex(None, node._left._left._left._left.previous_node())


previous_node_example1()

assert parse_node([[4, 5], [6, 7]])._left.next_node()._value == 6

assert (
    parse_node(
        [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    ).magnitude()
    == 3488
)


def explode_example1():
    node = parse_node([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    node._left._right._right._right.explode()
    assert node == parse_node([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])


def explode_example2():
    node = parse_node([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    node._right._right._right._right.explode()
    assert node == parse_node([[3, [2, [8, 0]]], [9, [5, [7, 0]]]])


explode_example1()
explode_example2()

aex(
    parse_node([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]).reduce(),
    parse_node([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]),
)


def parse_input(lines):
    result = []
    for line in lines:
        if isinstance(line, str):
            line = eval(line)
        result.append(parse_node(line))

    return result


TEST_NODES1 = parse_input(
    [
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 4],
        [5, 5],
        [6, 6],
    ]
)
TEST_RESULT1 = parse_node([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])
TEST_NODES2 = parse_input(
    [
        [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
        [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
        [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
        [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
        [7, [5, [[3, 8], [1, 4]]]],
        [[2, [2, 2]], [8, [8, 1]]],
        [2, 9],
        [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
        [[[5, [7, 4]], 7], 1],
        [[[[4, 2], 2], 6], [8, 7]],
    ]
)
TEST_RESULT2 = parse_node(
    [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
)

TEST_NODES5 = parse_input(
    [
        [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
        [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
        [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
        [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
        [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
        [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
        [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
        [[9, 3], [[9, 9], [6, [4, 9]]]],
        [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
        [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]],
    ]
)


def node_sum(data):
    result = data[0]
    for node in data[1:]:
        result += node

    return result


assrt(TEST_RESULT1, node_sum, TEST_NODES1)
assrt(TEST_RESULT2, node_sum, TEST_NODES2)

aex(
    parse_node(
        [[[[7, 8], [6, 6]], [[6, 0], [7, 7]]], [[[7, 8], [8, 8]], [[7, 9], [0, 6]]]]
    ),
    parse_node([[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]])
    + parse_node([[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]]),
)
aex(
    3993,
    parse_node(
        [[[[7, 8], [6, 6]], [[6, 0], [7, 7]]], [[[7, 8], [8, 8]], [[7, 9], [0, 6]]]]
    ).magnitude(),
)


def solve1(data):
    return node_sum(data).magnitude()


def solve2(data) -> int:
    result = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            a, b = data[i], data[j]
            result = max(result, max((a + b).magnitude(), (b + a).magnitude()))
    return result


assrt(4140, solve1, TEST_NODES5)

assrt(3993, solve2, TEST_NODES5)


def main():
    with open("in.txt") as infile:
        data = parse_input([line.strip() for line in infile.readlines()])
        print(solve1(data))
        print(solve2(data))


if __name__ == "__main__":
    main()
