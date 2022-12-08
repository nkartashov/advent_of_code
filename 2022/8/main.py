from typing import List, NamedTuple, Tuple, Dict
from enum import Enum

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def parse(lines: List[str]) -> List[List[int]]:
    return [[int(x) for x in line] for line in lines]


def solve1(lines: List[str]) -> int:
    trees = parse(lines)
    visible = [[False] * len(row) for row in trees]
    visible[0] = [True] * len(trees[0])
    visible[-1] = [True] * len(trees[-1])

    for row in visible:
        row[0] = True
        row[-1] = True

    # Visible from the top.
    heights = [x for x in trees[0]]
    for j in range(1, len(trees) - 1):
        for i, height in enumerate(trees[j]):
            visible[j][i] = visible[j][i] or height > heights[i]
            heights[i] = max(heights[i], height)

    # Visible from the bottom.
    heights = [x for x in trees[-1]]
    for j in range(len(trees) - 2, 0, -1):
        for i, height in enumerate(trees[j]):
            visible[j][i] = visible[j][i] or height > heights[i]
            heights[i] = max(heights[i], height)

    # Visible from the left.
    heights = [row[0] for row in trees]
    for i in range(1, len(trees[0]) - 1):
        for j in range(len(trees)):
            height = trees[j][i]
            visible[j][i] = visible[j][i] or height > heights[j]
            heights[j] = max(heights[j], height)

    # Visible from the right.
    heights = [row[-1] for row in trees]
    for i in range(len(trees[0]) - 2, 0, -1):
        for j in range(len(trees)):
            height = trees[j][i]
            visible[j][i] = visible[j][i] or height > heights[j]
            heights[j] = max(heights[j], height)

    return sum(sum(1 for x in row if x) for row in visible)


TEST_DATA = """30373
25512
65332
33549
35390""".split(
    "\n"
)

assrt(21, solve1, TEST_DATA)

NOT_SET = -2


def go_right(i: int, j: int, trees: List[List[int]], visible: List[List[int]]) -> int:
    if visible[j][i] == NOT_SET:
        height = trees[j][i]
        right_i = i + 1
        while right_i < len(trees[0]) and trees[j][right_i] < height:
            right_i = go_right(right_i, j, trees, visible)

        visible[j][i] = right_i

    return visible[j][i]


def go_left(i: int, j: int, trees: List[List[int]], visible: List[List[int]]) -> int:
    if visible[j][i] == NOT_SET:
        height = trees[j][i]
        left_i = i - 1
        while left_i >= 0 and trees[j][left_i] < height:
            left_i = go_left(left_i, j, trees, visible)

        visible[j][i] = left_i

    return visible[j][i]


def go_down(i: int, j: int, trees: List[List[int]], visible: List[List[int]]) -> int:
    if visible[j][i] == NOT_SET:
        height = trees[j][i]
        down_j = j + 1
        while down_j < len(trees) and trees[down_j][i] < height:
            down_j = go_down(i, down_j, trees, visible)

        visible[j][i] = down_j

    return visible[j][i]


def go_up(i: int, j: int, trees: List[List[int]], visible: List[List[int]]) -> int:
    if visible[j][i] == NOT_SET:
        height = trees[j][i]
        up_j = j - 1
        while up_j >= 0 and trees[up_j][i] < height:
            up_j = go_up(i, up_j, trees, visible)

        visible[j][i] = up_j

    return visible[j][i]


def solve2(lines: List[str]) -> int:
    trees = parse(lines)
    # Index of next tree on the right which is taller or equal.
    visible_right = [[NOT_SET] * len(row) for row in trees]
    for row in visible_right:
        row[-1] = len(trees[0])

    # Index of the next tree on the left which is taller or equal.
    visible_left = [[NOT_SET] * len(row) for row in trees]
    for row in visible_left:
        row[0] = -1

    # Index of next tree below which is taller or equal.
    visible_down = [[NOT_SET] * len(row) for row in trees]
    visible_down[-1] = [len(trees)] * len(trees[-1])

    # Index of next tree above which is taller or equal.
    visible_up = [[NOT_SET] * len(row) for row in trees]
    visible_up[0] = [-1] * len(trees[0])

    result = 0
    for j in range(len(trees)):
        for i in range(len(trees[0])):
            right_result = go_right(i, j, trees, visible_right)
            if right_result == len(trees[0]):
                right_result -= 1
            right_result -= i

            left_result = go_left(i, j, trees, visible_left)
            if left_result == -1:
                left_result += 1
            left_result = i - left_result

            down_result = go_down(i, j, trees, visible_down)
            if down_result == len(trees):
                down_result -= 1
            down_result -= j

            up_result = go_up(i, j, trees, visible_up)
            if up_result == -1:
                up_result += 1
            up_result = j - up_result

            result = max(result, left_result * right_result * down_result * up_result)

    return result


assrt(8, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
