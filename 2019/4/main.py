def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def join_number(number):
    power = 1
    result = 0
    for i in reversed(number):
        result += i * power
        power *= 10
    return result

ass(19870, join_number, [1, 9, 8, 7, 0])

def validate_number(current):
    duplicate = False
    for i in range(len(current) - 1):
        if current[i] == current[i + 1]:
            duplicate = True
    return 172851 < join_number(current) < 675869 and duplicate

def validate_number_2(current):
    collapsed = collapse(current)
    duplicate = any(count == 2 for _, count in collapsed)
    return 172851 < join_number(current) < 675869 and duplicate

def collapse(current):
    result = []
    i = 0
    while i < len(current):
        count = 1
        while i + count < len(current) and current[i] == current[i + count]:
            count += 1
        result.append((current[i], count))
        i += count
    return result

def generate_numbers(current):
    if len(current) == 6:
        if validate_number_2(current):
            return 1
        return 0
    result = 0
    for i in range(current[-1], 10):
        current.append(i)
        result += generate_numbers(current)
        current.pop()
    return result
    

def main():
    # 172851-675869
    low = 177777
    high = 669999
    result = 0
    for i in range(1, 7):
        result += generate_numbers([i])
    print(result)


if __name__ == "__main__":
    main()
