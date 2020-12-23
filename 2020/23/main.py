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

class Node:
    def __init__(self, value):
        self._value = value
        self._next = None

def get_cups(data):
    values = [int(ch) for ch in data]
    first = Node(values[0]) 
    current = first
    for value in values[1:]:
        node = Node(value)
        current._next = node
        current = current._next
    current._next = first
    return first

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
    for _ in range(moves):
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

    return produce_result(value_to_cup)

def produce_result(cup_map):
    current = cup_map[1]._next
    result = []
    while current != cup_map[1]:
        result.append(str(current._value))
        current = current._next

    return ''.join(result)

def get_test_data():
    return get_cups('389125467')

assrt('92658374', play, get_test_data(), 10)
assrt('67384529', play, get_test_data(), 100)

def main():
    input_data = '469217538'
    print(play(get_cups(input_data), 100))


if __name__ == "__main__":
    main()
