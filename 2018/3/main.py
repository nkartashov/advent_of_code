import sys
from typing import NamedTuple
from collections import defaultdict

MAX_SIZE = 1000

class Rect(NamedTuple):
    id: str
    start_x: int
    start_y: int
    width: int
    height: int

    def cell_count(self):
        return self.width * self.height

def ss(vals):
    return [x.strip() for x in vals]

def parse_rect(line):
    rect_id, rect_values = ss(line.split('@'))
    starts, sizes = rect_values.split(':')
    return Rect(
        rect_id,
        *[int(x.strip()) for x in starts.split(',')],
        *[int(x.strip()) for x in sizes.split('x')],
    )

def apply_rect(rect, field):
    for i in range(rect.start_x, rect.start_x + rect.width):
        for j in range(rect.start_y, rect.start_y + rect.height):
            if field[i][j] == '.':
                field[i][j] = rect.id
            else:
                field[i][j] = 'X'

def get_number_of_overlapped_cells(field):
    result = 0
    for row in field:
        for cell in row:
            if cell == 'X':
                result += 1
    return result

def get_non_overlapped_rect(field, rects):
    rect_cell_counts = defaultdict(int)
    for row in field:
        for cell in row:
            if cell != 'X' and cell != '.':
                rect_cell_counts[cell] += 1
    for rect_id, count in rect_cell_counts.items():
        if rects[rect_id].cell_count() == count:
            return rect_id

    return None

def main():
    field = [['.'] * MAX_SIZE for _ in range(MAX_SIZE)]
    rects = dict()
    for line in sys.stdin:
        rect = parse_rect(line)
        rects[rect.id] = rect
        apply_rect(rect, field)
    print(get_number_of_overlapped_cells(field))
    print(get_non_overlapped_rect(field, rects))


if __name__ == '__main__':
    main()
