import string

from utils import aex, splitlines, read_input

from pydantic import BaseModel

from enum import Enum
import math

class Colour(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"

class Game(BaseModel):
    id: int
    sets: list[dict[Colour, int]]


def parse_line(line: str) -> Game:
    id_side, cubes_side = line.split(':')
    id = int(id_side.split()[-1])
    sets = []
    for s_part in cubes_side.split(';'):
        parts = s_part.strip().split(', ')
        new_set = dict()
        for part in parts:
            cnt, colour = part.split()
            new_set[Colour(colour)] = int(cnt)
        sets.append(new_set)

    return Game(id=id, sets=sets)

aex(Game(id=1, sets=[
    {Colour.BLUE: 3, Colour.RED: 4},
    {Colour.GREEN: 2, Colour.RED: 1, Colour.BLUE: 6},
    {Colour.GREEN: 2},
]), parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"))




def solve1(lines: list[str]) -> int:
    games = [parse_line(line) for line in lines]
    res = 0
    for game in games:
        possible = True
        for s in game.sets:
            if s.get(Colour.RED, 0) > 12 or s.get(Colour.BLUE, 0) > 14 or s.get(Colour.GREEN, 0) > 13:
                possible = False
                break

        if possible:
            res += game.id
    return res

TEST_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

aex(8, solve1(splitlines(TEST_INPUT)))



def solve2(lines: list[str]) -> int:
    res = 0
    games = [parse_line(line) for line in lines]
    for game in games:
        cubes = dict()
        for s in game.sets:
            for colour, cnt in s.items():
                cubes[colour] = max(cubes.get(colour, 0), cnt)

        res += math.prod(cubes.values())

    return res

aex(2286, solve2(splitlines(TEST_INPUT)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))

if __name__ == "__main__":
    main()