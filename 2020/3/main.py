from typing import List

def count_trees(field: List[str], slope_x=3, slope_y=1) -> int:
    x, y = 0, 0
    result = 0
    while y + slope_y < len(field):
        x, y = (x + slope_x) % len(field[0]), y + slope_y
        if field[y][x] == '#':
            result += 1

    return result

TEST_FIELD1 = [
        "..##.",
        "#...#",
        ".#...",
]

assert(count_trees(TEST_FIELD1) == 1)

SLOPES = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
]

def count_trees_different_slopes(field: List[str]) -> int:
    result = 1
    for x, y in SLOPES:
        result *= count_trees(field, x, y)

    return result

def main():
    with open('in.txt') as infile:
        field = [line.strip() for line in infile.readlines()]
        print(count_trees(field))
        print(count_trees_different_slopes(field))


if __name__ == "__main__":
    main()
