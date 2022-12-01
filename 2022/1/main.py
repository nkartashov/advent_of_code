def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def get_elves(lines):
    result = []
    elf = []
    for line in lines:
        if line == "":
            result.append(elf)
            elf = []
        else:
            elf.append(int(line))
    if elf:
        result.append(elf)
    return result


def solve1(lines):
    elves = get_elves(lines)
    return max(sum(elf) for elf in elves)


TEST_LINES = [
    line.strip()
    for line in """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".split(
        "\n"
    )
]

assrt(24000, solve1, TEST_LINES)


def solve2(lines):
    elves = get_elves(lines)
    return sum(sorted((sum(elf) for elf in elves), reverse=True)[:3])


assrt(45000, solve2, TEST_LINES)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
