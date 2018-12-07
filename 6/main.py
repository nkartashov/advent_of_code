import sys

from typing import NamedTuple
from collections import defaultdict

class Coord(NamedTuple):
    x: int
    y: int

    def distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

def read_all_input():
    return [Coord(*map(int, line.strip().split(','))) for line in sys.stdin]

def compute_distances_from_points(x, y, points):
    distance_to_parent_idx = defaultdict(list)
    result = [0] * len(points)
    for i, point in enumerate(points):
        result[i] = point.distance(x, y)
    return result

def which_belongs(x, y, points):
    distances_from_points = compute_distances_from_points(x, y, points)
    min_dist = min(distances_from_points)
    possible_results = [i for i, dist in enumerate(distances_from_points) if dist == min_dist]
    if len(possible_results) > 1:
        return None
    return possible_results[0]

def idx_value_to_letter(value):
    if value is None:
        return '?'
    return chr(ord('a') + value)

def compute_area_sizes(minx, miny, maxx, maxy, points):
    area_sizes = [0] * len(points)
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            belongs = which_belongs(x, y, points)
            if belongs is not None:
                area_sizes[belongs] += 1
    return area_sizes

def find_points_with_infinite_area(minx, miny, maxx, maxy, points):
    result = set()
    for x in range(minx, maxx + 1):
        result.add(which_belongs(x, miny, points))
        result.add(which_belongs(x, maxy, points))
    for y in range(miny, maxy + 1):
        result.add(which_belongs(minx, y, points))
        result.add(which_belongs(maxx, y, points))
    return result


def choose_biggest_area(minx, miny, maxx, maxy, area_sizes, points_with_infinite_area):
    return max(area_size for i, area_size in enumerate(area_sizes) if i not in points_with_infinite_area)

def compute_largest_area(points):
    minx = min(point.x for point in points)
    miny = min(point.y for point in points)
    maxx = max(point.x for point in points)
    maxy = max(point.y for point in points)
    area_sizes = compute_area_sizes(minx, miny, maxx, maxy, points)
    points_with_infinite_area = find_points_with_infinite_area(minx, miny, maxx, maxy, points)
    return choose_biggest_area(minx, miny, maxx, maxy, area_sizes, points_with_infinite_area)

def compute_area_below_threshold(points, threshold=10000):
    minx = min(point.x for point in points)
    miny = min(point.y for point in points)
    maxx = max(point.x for point in points)
    maxy = max(point.y for point in points)
    result = 0
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            total_distance = sum(compute_distances_from_points(x, y, points))
            if total_distance < threshold:
                result += 1
    return result


assert compute_largest_area([
    Coord(1, 1),
    Coord(1, 6),
    Coord(8, 3),
    Coord(3, 4),
    Coord(5, 5),
    Coord(8, 9),
]) == 17
assert compute_area_below_threshold([
    Coord(1, 1),
    Coord(1, 6),
    Coord(8, 3),
    Coord(3, 4),
    Coord(5, 5),
    Coord(8, 9),
], 32) == 16


def main():
    points = read_all_input()
    print(compute_largest_area(points))
    print(compute_area_below_threshold(points))



if __name__ == '__main__':
    main()
