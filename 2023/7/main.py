import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import string
import math
from typing import Optional
from collections import Counter


class Kind(Enum):
    J = "J"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    T = "T"
    Q = "Q"
    K = "K"
    A = "A"

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            members = list(self.__class__)
            return members.index(self) < members.index(other)
        return NotImplemented


class Combination(Enum):
    FIVE_OF_A_KIND = 10
    FOUR_OF_A_KIND = 9
    FULL_HOUSE = 8
    THREE_OF_A_KIND = 7
    TWO_PAIRS = 6
    ONE_PAIR = 5
    HIGH_CARD = 4


class Hand(BaseModel):
    cards: list[Kind]
    bid: int
    support_jokers: bool = False

    def combination(self):
        c = Counter(self.cards)
        if self.support_jokers:
            joker_count = c.pop(Kind.J, 0)
            if joker_count:
                if joker_count >= 4:
                    return Combination.FIVE_OF_A_KIND

                if joker_count == 3:
                    if 2 in c.values():
                        return Combination.FIVE_OF_A_KIND
                    return Combination.FOUR_OF_A_KIND

                if joker_count == 2:
                    if 3 in c.values():
                        return Combination.FIVE_OF_A_KIND
                    if 2 in c.values():
                        return Combination.FOUR_OF_A_KIND
                    return Combination.THREE_OF_A_KIND

                if 4 in c.values():
                    return Combination.FIVE_OF_A_KIND
                if 3 in c.values():
                    return Combination.FOUR_OF_A_KIND
                if 2 in c.values() and len(c) == 2:
                    return Combination.FULL_HOUSE
                if 2 in c.values():
                    return Combination.THREE_OF_A_KIND
                return Combination.ONE_PAIR

        if 5 in c.values():
            return Combination.FIVE_OF_A_KIND
        if 4 in c.values():
            return Combination.FOUR_OF_A_KIND
        if 3 in c.values() and 2 in c.values():
            return Combination.FULL_HOUSE
        if 3 in c.values():
            return Combination.THREE_OF_A_KIND
        if 2 in c.values():
            if len(c) == 3:
                return Combination.TWO_PAIRS
            return Combination.ONE_PAIR

        return Combination.HIGH_CARD

    def __lt__(self, other: "Hand"):
        c1 = self.combination()
        c2 = other.combination()
        if c1 != c2:
            return c1.value < c2.value

        for a, b in zip(self.cards, other.cards):
            if a != b:
                return a < b

        return False


def parse_line(line: str, support_jokers: bool) -> Hand:
    cards = [Kind(c) for c in line.split()[0]]
    bid = int(line.split()[1])
    return Hand(cards=cards, bid=bid, support_jokers=support_jokers)


def parse_input(lines: list[str], support_jokers=False) -> list[Hand]:
    return [parse_line(l, support_jokers) for l in lines]


def solve1(lines: list[str]) -> int:
    hands = parse_input(lines)
    hands.sort()
    return sum(rank * hand.bid for rank, hand in enumerate(hands, 1))


TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

aex(6440, solve1(splitlines(TEST_INPUT)))


def solve2(lines: list[str]) -> int:
    hands = parse_input(lines, support_jokers=True)
    hands.sort()
    return sum(rank * hand.bid for rank, hand in enumerate(hands, 1))


aex(5905, solve2(splitlines(TEST_INPUT)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))


if __name__ == "__main__":
    main()
