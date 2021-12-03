from enum import Enum
from typing import NamedTuple, List, Tuple

def binary_to_decimal(value: str) -> int:
    return int(value, 2)

def compute_rates(numbers: List[str]) -> int:
    counts = [0] * len(numbers[0])
    for number in numbers:
        for i, x in enumerate(number):
            if x == '1':
                counts[i] += 1
    gamma = ['1' if x * 1.0 / len(numbers) > 0.5 else '0' for x in counts]
    epsilon = ['0' if x == '1' else '1' for x in gamma]
    return binary_to_decimal(''.join(gamma)) * binary_to_decimal(''.join(epsilon))

TEST_NUMBERS = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".split()
assert(compute_rates(TEST_NUMBERS) == 198)

def find_bit_counts(numbers: List[str], pos: int):
    result = [0, 0]
    for number in numbers:
        result[int(number[pos])] += 1
    return result

def filter_on_position(numbers: List[str], pos: int, bias: str) -> List[str]:
        counts = find_bit_counts(numbers, pos)
        if counts[0] != counts[1]:
            if bias == '1' and counts[0] > counts[1]:
                bias = '0'
            elif bias == '0' and counts[0] > counts[1]:
                bias = '1'
        return [number for number in numbers if number[pos] == bias]

def compute_rates2(numbers: List[str]) -> int:
    o2numbers = numbers
    pos = 0
    while len(o2numbers) > 1:
        o2numbers = filter_on_position(o2numbers, pos, '1')
        pos += 1

    co2numbers = numbers
    pos = 0
    while len(co2numbers) > 1:
        co2numbers = filter_on_position(co2numbers, pos, '0')
        pos += 1
    return binary_to_decimal(o2numbers[0]) * binary_to_decimal(co2numbers[0])

assert(compute_rates2(TEST_NUMBERS) == 230)


def main():
    with open('in.txt') as infile:
        numbers = [line.strip() for line in infile.readlines()]
        print(compute_rates(numbers))
        print(compute_rates2(numbers))


if __name__ == "__main__":
    main()
