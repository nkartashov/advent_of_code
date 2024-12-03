import string

from utils import aex, splitlines, read_input
from collections import Counter




def solve1(nums: list[tuple[int, int]]) -> int:
    xs, ys = [x for x, _ in nums], [y for _, y in nums]
    z = zip(sorted(xs), sorted(ys))
    return sum(abs(x - y) for x, y in z)

def parse_numbers(lines: list[str]) -> list[tuple[int, int]]:
    return [[int(x) for x in line.split()] for line in lines]

TEST_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3""".split('\n')
TEST_NUMS = parse_numbers(TEST_INPUT)

aex(11, solve1(TEST_NUMS))

def solve2(nums: list[tuple[int, int]]) -> int:
    xs, ys = [x for x, _ in nums], [y for _, y in nums]
    counts = Counter(ys)
    return sum(x * counts.get(x, 0) for x in xs)

aex(31, solve2(TEST_NUMS))

def main():
    lines = read_input("in.txt", __file__)
    nums = parse_numbers(lines)
    print(solve1(nums))
    print(solve2(nums))

if __name__ == "__main__":
    main()