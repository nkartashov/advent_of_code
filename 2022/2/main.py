from typing import List, NamedTuple
from enum import Enum


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @property
    def shape_cost(self):
        return self.value


OPPONENT_MOVES = {
    "A": Move.ROCK,
    "B": Move.PAPER,
    "C": Move.SCISSORS,
}

YOUR_MOVES = {
    "X": Move.ROCK,
    "Y": Move.PAPER,
    "Z": Move.SCISSORS,
}


class Round(NamedTuple):
    opponent: Move
    you: Move


def parse_rounds(moves) -> List[Round]:
    result = []
    for opponent, you in moves:
        result.append(Round(opponent=OPPONENT_MOVES[opponent], you=YOUR_MOVES[you]))
    return result


WINNING_MOVES = {
    (Move.PAPER, Move.ROCK),
    (Move.ROCK, Move.SCISSORS),
    (Move.SCISSORS, Move.PAPER),
}


def solve1(lines):
    rounds = parse_rounds(lines)
    result = 0
    for r in rounds:
        result += r.you.shape_cost
        if r.you == r.opponent:
            result += 3
        elif (r.you, r.opponent) in WINNING_MOVES:
            result += 6

    return result


TEST_LINES = [
    line.strip().split()
    for line in """A Y
B X
C Z""".split(
        "\n"
    )
]

assrt(15, solve1, TEST_LINES)


class Result(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"

    @property
    def cost(self):
        if self == Result.DRAW:
            return 3
        if self == Result.WIN:
            return 6
        return 0


class Round2(NamedTuple):
    opponent: Move
    result: Result


def parse_rounds2(lines) -> List[Round2]:
    result = []
    for opponent, r in lines:
        result.append(Round2(opponent=OPPONENT_MOVES[opponent], result=Result(r)))
    return result


MOVE_AND_RESULT = {
    (Move.ROCK, Result.WIN): Move.PAPER,
    (Move.PAPER, Result.WIN): Move.SCISSORS,
    (Move.SCISSORS, Result.WIN): Move.ROCK,
    (Move.ROCK, Result.LOSE): Move.SCISSORS,
    (Move.PAPER, Result.LOSE): Move.ROCK,
    (Move.SCISSORS, Result.LOSE): Move.PAPER,
}


def solve2(lines):
    rounds = parse_rounds2(lines)
    result = 0
    for r in rounds:
        result += r.result.cost
        if r.result == Result.DRAW:
            result += r.opponent.shape_cost
            continue
        result += MOVE_AND_RESULT[(r.opponent, r.result)].shape_cost

    return result


assrt(12, solve2, TEST_LINES)


def main():
    with open("in.txt") as infile:
        lines = [line.strip().split() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
