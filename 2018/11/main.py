from tqdm import trange

FIELD_SIZE = 300

def compute_level(x, y, serial_number):
    rack_id = x + 10
    power_level = (rack_id * y + serial_number) * rack_id
    digit = (power_level // 100) % 10
    return digit - 5

assert compute_level(3, 5, 8) == 4
assert compute_level(122, 79, 57) == -5
assert compute_level(217, 196, 39) == 0
assert compute_level(101, 153, 71) == 4

def build_field(serial_number):
    result = [[None] * FIELD_SIZE for _ in range(FIELD_SIZE)]
    for y in range(1, FIELD_SIZE + 1):
        for x in range(1, FIELD_SIZE + 1):
            result[y - 1][x - 1] = compute_level(x, y, serial_number)
    return result

def compute_square_sum(field, x, y, size=3):
    return sum(sum(row[x: x + size]) for row in field[y: y + size])

def find_square_with_largest_power(field):
    result = None, None
    max_sum = -1000000000000000
    for y in range(FIELD_SIZE - 2):
        for x in range(FIELD_SIZE - 2):
            square_sum = compute_square_sum(field, x, y)
            if square_sum > max_sum:
                max_sum = square_sum
                result = x + 1, y + 1
    return result

field18 = build_field(18)
assert find_square_with_largest_power(field18) == (33, 45)
field42 = build_field(42)
assert find_square_with_largest_power(field42) == (21, 61)

def compute_row_sum(row):
    result = [0] * len(row)
    current = 0
    for i, val in enumerate(row):
        current += val
        result[i] = current
    return result

assert compute_row_sum([1, 2, -1, 3, 51]) == [1, 3, 2, 5, 56]

def compute_row_sums(field):
    return [compute_row_sum(row) for row in field]

def compute_aux_square_sums(field):
    row_sums = compute_row_sums(field)
    result = compute_row_sums(field)
    for y in range(1, len(field)):
        for x in range(len(field[0])):
            result[y][x] = result[y - 1][x] + row_sums[y][x]
    return result

test_field = [
    [1, 2],
    [3, 4],
]
assert compute_aux_square_sums(test_field) == [
    [1, 3],
    [4, 10],
]
    
def compute_square_sum_with_aux_sums(x, y, size, aux_sums):
    assert x + size <= FIELD_SIZE
    assert y + size <= FIELD_SIZE
    result = aux_sums[y + size - 1][x + size - 1]
    if y != 0:
        result -= aux_sums[y - 1][x + size - 1]
    if x != 0:
        result -= aux_sums[y + size - 1][x - 1]
    if x != 0 and y != 0:
        result += aux_sums[y - 1][x - 1]
    return result

def find_square_with_largest_power_with_variable_size(field):
    aux_sums = compute_aux_square_sums(field)
    result = None, None
    max_sum = -1000000000000000
    for size in trange(1, FIELD_SIZE + 1):
        for y in range(FIELD_SIZE - size - 1):
            for x in range(FIELD_SIZE - size - 1):
                square_sum = compute_square_sum_with_aux_sums(x, y, size, aux_sums)
                if square_sum > max_sum:
                    max_sum = square_sum
                    result = x + 1, y + 1, size
    return result

# assert find_square_with_largest_power_with_variable_size(field18) == (90, 269, 16)
# assert find_square_with_largest_power_with_variable_size(field42) == (232, 251, 12)

def main():
    serial_number = 8561
    field = build_field(serial_number)
    print(find_square_with_largest_power(field))
    print(find_square_with_largest_power_with_variable_size(field))

if __name__ == '__main__':
    main()
