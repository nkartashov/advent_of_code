import sys
import time
import copy

def read_input():
    return parse_input(sys.stdin.readlines())

def parse_pair(text):
    return [int(value.strip()) for value in text.split('<')[1][:-1].split(',')]

assert parse_pair('=< 0,  2>') == [0, 2]

def parse_input(lines):
    coordinates = []
    velocities = []
    for line in lines:
        coordinate, velocity = [parse_pair(piece.strip()) for piece in line.split('velocity')]
        coordinates.append(coordinate)
        velocities.append(velocity)

    return coordinates, velocities

assert parse_input(
    ["position=< 9,  1> velocity=< 0,  2>"]
) == ([[9, 1]], [[0, 2]])


def get_approximate_bounding_box_size(coordinates):
    minx = min(x for x, y in coordinates)
    miny = min(y for x, y in coordinates)
    maxx = max(x for x, y in coordinates)
    maxy = max(y for x, y in coordinates)
    return (maxx - minx) * (maxy - miny)

def draw_message(coordinates):
    minx = min(x for x, y in coordinates)
    miny = min(y for x, y in coordinates)
    maxx = max(x for x, y in coordinates)
    maxy = max(y for x, y in coordinates)
    field = [['.'] * (maxx - minx + 1) for _ in range(maxy - miny + 1)]
    for x, y in coordinates:
        field[y - miny][x - minx] = '#'
    print('\n'.join(''.join(row) for row in field))
    print()

def run_tick(coordinates, velocities):
    result = []
    for i, (x, y) in enumerate(coordinates):
        vx, vy = velocities[i]
        result.append((x + vx, y + vy))
    return result

def play_message(coordinates, velocities):
    tick_count = 0
    for tick in range(1, 1000000000):
        coordinates = run_tick(coordinates, velocities)
        box_size = get_approximate_bounding_box_size(coordinates)
        if box_size < 1000:
            draw_message(coordinates)
            print(tick)
            break

def main():
    values = read_input()
    play_message(*values)


if __name__ == '__main__':
    main()
