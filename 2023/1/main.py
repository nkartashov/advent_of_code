import string

from utils import aex, splitlines, read_input




def solve1(lines: list[str]) -> int:
    res = 0
    for line in lines:
        digits = ''.join(filter(lambda x: x not in string.ascii_letters, line))
        res += int(digits[0] + digits[-1])

    return res

TEST_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

aex(142, solve1(splitlines(TEST_INPUT)))

DIGITS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'one': 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find_digits(line: str) -> list[int]:
    res = []
    i = 0
    while i < len(line):
        for d in DIGITS:
            if line[i:].startswith(d):
                res.append(DIGITS[d])
                break
        i += 1

    return res

aex([1, 2], find_digits("1abc2"))
aex([2, 1, 9], find_digits("two1nine")) 
aex([8, 2, 3], find_digits("eightwothree"))


def solve2(lines: list[str]) -> int:
    res = 0
    for line in lines:
        digits = find_digits(line)
        res += digits[0] * 10 + digits[-1]

    return res

TEST_INPUT2= """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

aex(281, solve2(splitlines(TEST_INPUT2)))


def main():
    lines = read_input("in.txt", __file__)
    print(solve1(lines))
    print(solve2(lines))

if __name__ == "__main__":
    main()