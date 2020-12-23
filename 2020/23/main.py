from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache
from tqdm import tqdm

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def set_sum(args):
    result = set()
    for arg in args:
        result = result | arg
    return result

class Node:
    def __init__(self, value):
        self._value = value
        self._next = None

def get_cups(data, total_values=0):
    values = [int(ch) for ch in data]
    fake = Node(-1)
    current = fake

    def add_node(value):
        node = Node(value)
        current._next = node
        return current._next

    values_to_populate = values + [i for i in range(len(values) + 1, total_values + 1)]
    assert(len(values_to_populate) == max(len(values), total_values))

    for value in values_to_populate:
        current = add_node(value)

    current._next = fake._next
    return fake._next

def get_cup_map(first_cup):
    current = first_cup
    result = dict()
    while True:
        result[current._value] = current
        if current._next == first_cup:
            break
        current = current._next
    return result

def play(first_cup, moves):
    current = first_cup
    value_to_cup = get_cup_map(first_cup)
    for _ in tqdm(range(moves)):
        taken = current._next
        current._next = taken._next._next._next
        dest_value = current._value
        while True:
            dest_value -= 1
            if dest_value < 1:
                dest_value += 9
            if dest_value not in {taken._value, taken._next._value, taken._next._next._value}:
                break
        dest = value_to_cup[dest_value]
        old_dest_next = dest._next
        dest._next = taken
        taken._next._next._next = old_dest_next
        current = current._next

    return value_to_cup

def part1(first_cup, moves):
    return produce_result(play(first_cup, moves))


def produce_result(cup_map):
    current = cup_map[1]._next
    result = []
    while current != cup_map[1]:
        result.append(str(current._value))
        current = current._next

    return ''.join(result)

def get_test_data(total_values=0):
    return get_cups('389125467', total_values=total_values)

assrt('92658374', part1, get_test_data(), 10)
assrt('67384529', part1, get_test_data(), 100)

def part2(first_cup):
    value_to_cup = play(first_cup, 10 ** 7)
    first_cup = value_to_cup[1]._next
    second_cup = first_cup._next
    return first_cup._value * second_cup._value

assrt(149245887792, part2, get_test_data(10 ** 6))

def main():
    input_data = '469217538'
    print(part1(get_cups(input_data), 100))
    print(part2(get_cups(input_data, 10 ** 6)))


if __name__ == "__main__":
    main()
