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

class Paren(Enum):
    LEFT = '('
    RIGHT = ')'

    @classmethod
    def values(cls):
        return [p.value for p in cls]

class Op(Enum):
    MULT = '*'
    SUM = '+'

    @classmethod
    def values(cls):
        return [p.value for p in cls]

class Token(NamedTuple):
    int_val: int = None
    paren: Paren = None
    op: Op = None

def tokenize_expression(expression):
    tokens = []
    i = 0

    def parse_int(start):
        i = start
        while i < len(expression) and expression[i].isnumeric():
            i += 1
        return int(expression[start : i]), i

    while i < len(expression):
        if expression[i].isnumeric():
            int_val, i = parse_int(i)
            tokens.append(Token(int_val=int_val))
            continue 

        if expression[i] in Paren.values():
            tokens.append(Token(paren=Paren(expression[i])))

        if expression[i] in Op.values():
            tokens.append(Token(op=Op(expression[i])))

        i += 1
    return tokens

assrt([
    Token(int_val=22), Token(op=Op.MULT), Token(int_val=3),
    Token(op=Op.SUM), Token(paren=Paren.LEFT), Token(int_val=4),
    Token(op=Op.MULT), Token(int_val=5), Token(paren=Paren.RIGHT)
], tokenize_expression, "22 * 3 + (4 * 5)")


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]


if __name__ == "__main__":
    main()
