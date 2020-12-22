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
    ingredients: Set[str]
    allergens: Set[str]

def parse_line(line):
    ingredient_string, allergen_string = line.split('(contains')
    return Dish(
        ingredients=set(ingredient_string.strip().split()),
        allergens=set(allergen_string[:-1].strip().split(', '))
    )


TEST_STRING1 = 'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)'
TEST_DISH1 = Dish(
    ingredients={'mxmxvkd', 'kfcds', 'sqjhc', 'nhms'},
    allergens={'dairy', 'fish'},
)

TEST_STRING2 = 'trh fvjkl sbzzf mxmxvkd (contains dairy)'
TEST_DISH2 = Dish(
    ingredients={'trh', 'fvjkl', 'sbzzf', 'mxmxvkd'},
    allergens={'dairy'}
)

assrt(TEST_DISH1, parse_line, TEST_STRING1)
assrt(TEST_DISH2, parse_line, TEST_STRING2)

def reconsile_dishes(dishes):
    all_allergens = set_sum(dish.allergens for dish in dishes)
    all_ingredients = set_sum(dish.ingredients for dish in dishes)
    ingredients_with_known_allergens = dict()
    known_allergens = set()
    allergen_to_dish = defaultdict(list)
    for dish in dishes:
        for allergen in dish.allergens:
            allergen_to_dish[allergen].append(dish)

    have_updated = True
    while have_updated:
        have_updated = False
        for allergen, dishes in allergen_to_dish.items():
            if allergen in known_allergens:
                continue
            possible_ingredients = deepcopy(all_ingredients) - set(ingredients_with_known_allergens.keys())
            for dish in dishes:
                possible_ingredients &= dish.ingredients
                if len(possible_ingredients) == 1:
                    have_updated = True
                    ingredient, = possible_ingredients
                    ingredients_with_known_allergens[ingredient] = allergen
                    known_allergens.add(allergen)
                    break

    return ingredients_with_known_allergens

def count_ingredients_with_no_known_allergens(dishes, ingredients_with_known_allergens):
    result = 0
    for dish in dishes:
        result += sum(1 for ingredient in dish.ingredients if ingredient not in ingredients_with_known_allergens)
    return result



def read_input(filename='in.txt'):
    with open(filename) as infile:
        return [parse_line(line.strip()) for line in infile.readlines()]

TEST_DISHES = read_input(filename='test_dishes.txt')
assrt(5, count_ingredients_with_no_known_allergens, TEST_DISHES, reconsile_dishes(TEST_DISHES))


def main():
    dishes = read_input()
    known_allergens = reconsile_dishes(dishes)
    print(count_ingredients_with_no_known_allergens(dishes, known_allergens))


if __name__ == "__main__":
    main()
