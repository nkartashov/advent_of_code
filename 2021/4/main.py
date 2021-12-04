from enum import Enum
from typing import NamedTuple, List, Tuple

BOARD_SIZE = 5


class Board:
    def __init__(self, values):
        self._values = values
        self._marked = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def mark(self, value):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self._values[i][j] == value:
                    self._marked[i][j] = True

    def is_bingo(self):
        return (
            # rows
            any(all(self._marked[i]) for i in range(BOARD_SIZE))
            # columns
            or any(all(row[i] for row in self._marked) for i in range(BOARD_SIZE))
        )

    def count_score(self):
        return sum(
            sum(self._values[i][j] for i in range(BOARD_SIZE) if not self._marked[i][j])
            for j in range(BOARD_SIZE)
        )

    def __repr__(self):
        return "\n".join(" ".join(str(x) for x in line) for line in self._values)


def find_first_to_win(numbers: List[int], boards: List[Board]) -> int:
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.is_bingo():
                return board.count_score() * number
    assert False


def find_last_to_win(numbers: List[int], boards: List[Board]) -> int:
    last_bingo_board = None
    last_number = None
    for number in numbers:
        new_boards = []
        for board in boards:
            board.mark(number)
            if board.is_bingo():
                last_bingo_board = board
            else:
                new_boards.append(board)
        if not new_boards:
            last_number = number
            break
        boards = new_boards

    assert last_bingo_board is not None
    assert last_number is not None
    return last_bingo_board.count_score() * last_number


def read_input():
    with open("in.txt") as infile:
        numbers = [int(value) for value in infile.readline().split(",")]
        board_lines = [line.strip() for line in infile.readlines()]
        boards = []
        i = 1
        while i < len(board_lines):
            boards.append(
                Board(
                    [
                        [int(value) for value in line.split()]
                        for line in board_lines[i : i + BOARD_SIZE]
                    ]
                )
            )
            i += BOARD_SIZE + 1
        return numbers, boards


def main():
    print(find_first_to_win(*read_input()))
    print(find_last_to_win(*read_input()))


if __name__ == "__main__":
    main()
