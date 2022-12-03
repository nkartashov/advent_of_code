from typing import NamedTuple, Mapping
from enum import Enum
import itertools

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Loc(NamedTuple):
    x: int
    y: int

    def add_direction(self, direction: Direction) -> 'Loc':
        if direction == UP:
            return Loc(self.x, self.y - 1)
        if direction == RIGHT:
            return Loc(self.x + 1, self.y)
        if direction == DOWN:
            return Loc(self.x, self.y + 1)
        return Loc(self.x - 1, self.y)

class Cart:
    def __init__(self, loc: Loc, direction: Direction):
        self._loc = loc
        self._direction = direction
        self._turn_counter = itertools.cycle([-1, 0, 1])

    def process_interaction(self, other):
        self.loc = self.loc.add_direction(self.direction)
        if isinstance(other, Cart):
            return True
        if isinstance(other, Turn):
            self._direction = other.turn_map[self._direction]
        if isinstance(other, Crossing):
            self._direction = Direction((self._direction.value + self._next_turn) % len(Direction))
        return False

    def _next_turn(self):
        return next(self._turn_counter)

class Turn(NamedTuple):
    loc: Loc
    turn_map: Mapping[Direction, Direction]

class Crossing(NamedTuple):
    loc: Loc


