import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math


class Card(BaseModel):
    id: int
    numbers: list[int]
    winning_numbers: list[int]

    def get_matches(self) -> list[int]:
        res = []
        for n in self.numbers:
            if n in self.winning_numbers:
                res.append(n)

        return res

    def get_score(self) -> int:
        matches = self.get_matches()
        if len(matches) == 0:
            return 0
        
        return 2 ** (len(matches) - 1)
  

aex(8, Card(id=1, numbers=[41,48,83,86,17], winning_numbers=[83,86 ,6,31,17, 9,48,53]).get_score())

def parse_line(line: str) -> Card:
    id_side, numbers_side = line.split(':')
    id = int(id_side.split()[-1])
    numbers_side, winning_numbers_side = numbers_side.strip().split('|')
    return Card(
        id=id,
        numbers=[int(x) for x in numbers_side.strip().split()],
        winning_numbers=[int(x) for x in winning_numbers_side.strip().split()]
    )



def solve1(lines: list[str]) -> int:
    cards = [parse_line(line) for line in lines]
    return sum(c.get_score() for c in cards)

TEST_INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

aex(13, solve1(splitlines(TEST_INPUT)))

def process_card(cards: dict[int, Card], current: int, cache) -> int:
    if current not in cache:
        total = 1
        current_card = cards[current]
        matches = current_card.get_matches()
        for x in range(len(matches)):
            total += process_card(cards, current + x + 1, cache)
        cache[current] = total

    return cache[current]

def solve2(lines: list[str]) -> int:
    cards = [parse_line(line) for line in lines]
    cards = {c.id: c for c in cards}

    cache = dict()
    return sum(process_card(cards, x, cache) for x in cards.keys())



aex(30, solve2(splitlines(TEST_INPUT)))

def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))

if __name__ == "__main__":
    main()