import string

from utils import aex, splitlines, read_input
from collections import Counter
from dataclasses import dataclass

@dataclass
class Mul:
    x: int
    y: int


TOKENS = ['mul(', ',', ')']

def try_parse_int(s: str) -> None:
    try:
        return int(s)
    except ValueError:
        return None


def parse_mul(s: str, idx: int) -> tuple[None | Mul, int]:
    tok_idx = 0
    if not s.startswith(TOKENS[tok_idx], idx):
        return None, idx + 1
    idx += len(TOKENS[tok_idx])
    tok_idx += 1

    next_idx = s.find(TOKENS[tok_idx], idx)
    if next_idx == -1:
        return None, idx
    
    x = try_parse_int(s[idx:next_idx])
    if x is None:
        return None, idx
    
    idx = 


def solve1(text: list[str]) -> int:
    return 2

TEST_INPUT = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""".split('\n')

aex(161, solve1(TEST_INPUT))



def solve2(text: list[str]) -> int:
    return 4

aex(4, solve2(TEST_INPUT))

def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))

if __name__ == "__main__":
    main()