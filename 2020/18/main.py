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

# Left paren -> corresponding right paren
def get_paren_idxs(tokens):
    result = dict()
    stack = []
    for i, token in enumerate(tokens):
        if token.paren == Paren.RIGHT:
            result[stack.pop()] = i
        if token.paren == Paren.LEFT:
            stack.append(i)
    return result
        

def eval_expression(tokens):
    return eval_expression_helper(tokens, 0, len(tokens), get_paren_idxs(tokens))

def eval_expression_helper(tokens, start, end, paren_idxs):
    result = 0
    i = start

    def eval_arg(i):
        if tokens[i].int_val is not None:
            return tokens[i].int_val, i + 1

        # It can only be a parenthesized expression.
        return eval_expression_helper(tokens, i + 1, paren_idxs[i], paren_idxs), paren_idxs[i] + 1
        
    result, i = eval_arg(i)

    while i < end:
        op = tokens[i]
        right_arg, i = eval_arg(i + 1)
        if op.op == Op.SUM:
            result += right_arg
        else:
            result *= right_arg

    return result

assrt(26, eval_expression, tokenize_expression('2 * 3 + (4 * 5)'))
assrt(13632, eval_expression, tokenize_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))

def eval_all(lines, eval_func=eval_expression):
    return sum(eval_func(tokenize_expression(line)) for line in lines)

def eval_expression_advanced(tokens):
    return eval_expression_helper_advanced(tokens, 0)[0]

def eval_expression_helper_advanced(tokens, start):
    def eval_arg(i):
        if tokens[i].int_val is not None:
            return tokens[i].int_val, i + 1

        # It can only be a parenthesized expression.
        result, new_i = eval_expression_helper_advanced(tokens, i + 1)
        return result, new_i + 1

    def has_note_finished(i):
        return i < len(tokens) and tokens[i].paren != Paren.RIGHT

    result, i = eval_arg(start)
    # term * term
    current_terms = []
    while has_note_finished(i):
        op = tokens[i]
        if op.op == Op.SUM:
            right_arg, i = eval_arg(i + 1)
            result += right_arg
        else:
            current_terms.append(result)
            result, i = eval_arg(i + 1)

    current_terms.append(result)
        
    result = 1
    for term in current_terms:
        result *= term

    return result, i

assrt(669060, eval_expression_advanced, tokenize_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
assrt(23340, eval_expression_advanced, tokenize_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(eval_all(lines))
        print(eval_all(lines, eval_func=eval_expression_advanced))


if __name__ == "__main__":
    main()
