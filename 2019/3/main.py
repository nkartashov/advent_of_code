from typing import NamedTuple
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class Move(NamedTuple):
    direction: str
    length: int

DIRECTIONS = 'UDRL'

DIRECTION_VECTORS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

def parse_movement(move):
    return Move(direction=move[0], length=int(move[1:]))

def draw_wire(start, grid, wire, wire_id):
    intersections = []
    current = start
    steps = 0
    for move in wire:
        direction_vector = DIRECTION_VECTORS[DIRECTIONS.index(move.direction)]

        for _ in range(move.length):
            steps += 1
            current = current[0] + direction_vector[0], current[1] + direction_vector[1]
            if current in grid and grid[current][1] != wire_id:
                intersections.append((current, grid[current][0] + steps))
            elif current not in grid:
                grid[current] = steps, wire_id
    return intersections

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def main():
    with open('in.txt') as infile:
        wires = [[parse_movement(move) for move in line.strip().split(',')] for line in infile.readlines()]
        intersections = []
        grid = dict()
        for i, wire in enumerate(wires):
            res = draw_wire((0, 0), grid, wire, i)
            intersections.extend(res)
        intersections = [(intersection, steps) for intersection, steps in intersections if intersection != (0, 0)]
        closest_intersection = intersections[0][0]
        for intersection, _ in intersections:
            if manhattan_distance(intersection, (0, 0)) < manhattan_distance(closest_intersection, (0, 0)):
                closest_intersection = intersection
        print(manhattan_distance(closest_intersection, (0, 0)))
        print(min(intersections, key=lambda x: x[1]))


if __name__ == "__main__":
    main()
