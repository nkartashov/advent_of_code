from typing import List, NamedTuple

ROW_BITS = 7
COLUMN_BITS = 3
MAX_COLUMNS = 2 ** COLUMN_BITS


def parse_row_encoding(row_code) -> int:
    def mapper(x):
        if x == "B":
            return "1"
        return "0"

    return int(''.join(mapper(x) for x in row_code), 2)

assert(parse_row_encoding("FBFBBFF") == 44)

def parse_column_encoding(column_code) -> int:
    def mapper(x):
        if x == "R":
            return "1"
        return "0"

    return int(''.join(mapper(x) for x in column_code), 2)

assert(parse_column_encoding("RLR") == 5)


class BoardingPass(NamedTuple):
    row: int
    column: int

    @staticmethod
    def parse(code) -> "BoardingPass":
        return BoardingPass(
                row=parse_row_encoding(code[:ROW_BITS]),
                column=parse_column_encoding(code[ROW_BITS:])
        )

    @property
    def seat_id(self):
        return self.row * MAX_COLUMNS + self.column

assert(BoardingPass.parse("FBFBBFFRLR").seat_id == 357)

def parse_passes(lines):
    return [BoardingPass.parse(line) for line in lines]

def find_missing_seat(passes):
    seat_ids = [pazz.seat_id for pazz in passes]
    seat_ids.sort()
    for i, seat_id in enumerate(seat_ids):
        # No need to check for bounds as solution exists in the list
        if seat_ids[i + 1] == seat_id + 2:
            return seat_id + 1

    return None

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        passes = parse_passes(lines)
        print(max(pazz.seat_id for pazz in passes))
        print(find_missing_seat(passes))


if __name__ == "__main__":
    main()
