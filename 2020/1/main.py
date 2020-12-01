import bisect as bs

def find_two_summing_to_target(values, target):
    for i, value in enumerate(values):
        value_to_find = target - value
        found_position = bs.bisect_left(values, value_to_find, i + 1)
        if found_position != len(values) and values[found_position] == value_to_find:
            return value, value_to_find
    return None, None

assert(find_two_summing_to_target([], 1) == (None, None))
assert(find_two_summing_to_target([1, 1], 2) == (1, 1))
assert(find_two_summing_to_target([-2, 1, 2], 2) == (None, None))
assert(find_two_summing_to_target([-2, 1, 2], -1) == (-2, 1))

def find_three_summing_to_target(values, target):
    for i, value in enumerate(values):
        x, y = find_two_summing_to_target(values[i+1:], target - value)
        if x is not None:
            return value, x, y
    return None, None, None

assert(find_three_summing_to_target([], 1) == (None, None, None))
assert(find_three_summing_to_target([1, 1, 1], 3) == (1, 1, 1))
assert(find_three_summing_to_target([-2, 1, 2], 2) == (None, None, None))
assert(find_three_summing_to_target([-2, -1, 1, 2, 4], 5) == (-1, 2, 4))


def main():
    with open('in.txt') as infile:
        values = list(sorted([int(line.strip()) for line in infile.readlines()]))
        x, y = find_two_summing_to_target(values, 2020)
        print(x * y)
        x, y, z = find_three_summing_to_target(values, 2020)
        print(x * y * z)


if __name__ == "__main__":
    main()
