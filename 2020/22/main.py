from typing import List, NamedTuple, Set, Tuple, Dict
from enum import Enum
from collections import defaultdict, deque
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

def calculate_score(deck):
    result = 0
    for i, card in enumerate(deck):
        result += card * (len(deck) - i)
    return result

assrt(306, calculate_score, [3, 2, 10, 6, 8, 5, 9, 4, 7, 1])

def play(p1, p2):
    d1, d2 = deque(p1), deque(p2)
    while d1 and d2:
        x, y = d1.popleft(), d2.popleft()
        if x > y:
            d1.extend([x, y])
        else:
            d2.extend([y, x])

    winner = d1
    if d2:
        winner = d2
    return calculate_score(winner)

assrt(306, play, [9, 2, 6, 3, 1], [5, 8, 4, 7, 10])



def main():
    p1 = None
    with open('player1.txt') as infile:
        p1 = [int(line.strip()) for line in infile.readlines()]

    p2 = None
    with open('player2.txt') as infile:
        p2 = [int(line.strip()) for line in infile.readlines()]

    print(play(p1, p2))



if __name__ == "__main__":
    main()
