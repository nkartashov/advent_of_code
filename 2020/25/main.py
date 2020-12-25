from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache
from tqdm import tqdm
import math

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def set_sum(args):
    result = set()
    for arg in args:
        result = result | arg
    return result

M = 20201227
G = 7


# a ^ x = b (mod m)
def find_power(b, a=G, m=M):
    n = int(math.sqrt(m)) + 1
    values = dict()
    for i in reversed(range(1, n + 1)):
        values[pow(a, i * n, m)] = i
    for i in range(n + 1):
        cur = (pow(a, i, m) * b) % m
        if cur in values:
            result = values[cur] * n - i
            if result < m:
                return result
    return None

assrt(8, find_power, 5764801)

def part1(input_data):
    card_pk, door_pk = input_data
    card_loop = find_power(card_pk)
    assert card_loop is not None
    return pow(door_pk, card_loop, M)


def read_input(filename='in.txt'):
    with open(filename) as infile:
        return [int(line.strip()) for line in infile.readlines()]

def main():
    input_data = read_input()
    print(part1(input_data))


if __name__ == "__main__":
    main()
