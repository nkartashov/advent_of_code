from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def set_sum(args):
    result = set()
    for arg in args:
        result = result | arg
    return result

class Dish(NamedTuple):
    ingredients: List[str]
    allergens: List[str]

def parse_line(line):
    ingredient_string, allergen_string = line.split('(contains')
    return Dish(ingredients=ingredient_string.strip().split(), allergens=allergen_string[:-1].strip().split(', '))

TEST_STRING1 = 'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)'
TEST_DISH1 = Dish(
    ingredients=['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'],
    allergens=['dairy', 'fish'],
)

TEST_STRING2 = 'trh fvjkl sbzzf mxmxvkd (contains dairy)'
TEST_DISH2 = Dish(
    ingredients=['trh', 'fvjkl', 'sbzzf', 'mxmxvkd'],
    allergens=['dairy']
)

assrt(TEST_DISH1, parse_line, TEST_STRING1)
assrt(TEST_DISH2, parse_line, TEST_STRING2)


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]


if __name__ == "__main__":
    main()
