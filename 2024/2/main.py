import string

from utils import aex, splitlines, read_input
from collections import Counter

def is_increasing(nums: list[int]) -> bool:
    for prev, x in zip(nums, nums[1:]):
        if prev >= x:
            return False
        
    return True

def is_safe(nums: list[int]) -> bool:
    monotonic = is_increasing(nums) or is_increasing(list(reversed(nums)))
    if not monotonic:
        return False
    
    for prev, x in zip(nums, nums[1:]):
        if not (1 <= abs(prev - x) <= 3):
            return False
        
    return True
    


def solve1(nums: list[list[int, int]]) -> int:
    result = 0
    for l in nums:
        if is_safe(l):
            result += 1

    return result

def parse_numbers(lines: list[str]) -> list[list[int, int]]:
    return [[int(x) for x in line.split()] for line in lines]

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".split('\n')
TEST_NUMS = parse_numbers(TEST_INPUT)

aex(2, solve1(TEST_NUMS))

def is_safe2(nums: list[int]) -> bool:
    return any(
        is_safe(nums[:i] + nums[i + 1:]) for i in range(len(nums))
    )

def solve2(nums: list[list[int, int]]) -> int:
    result = 0
    for l in nums:
        if is_safe2(l):
            result += 1

    return result

aex(4, solve2(TEST_NUMS))

def main():
    lines = read_input("in.txt", __file__)
    nums = parse_numbers(lines)
    print(solve1(nums))
    print(solve2(nums))

if __name__ == "__main__":
    main()