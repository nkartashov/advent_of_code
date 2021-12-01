

def count_increases(values):
    result = 0
    for i in range(1, len(values)):
        if values[i] - values[i - 1] > 0:
            result += 1
    return result

def count_increases_sliding(values, window=2):
    result = 0
    for i in range(window + 1, len(values)):
        cur_sum = sum(values[i - window:i + 1])
        prev_sum = sum(values[i - window - 1:i])
        if  cur_sum - prev_sum > 0:
            result += 1
    return result

def main():
    with open('in.txt') as infile:
        values = [int(line.strip()) for line in infile.readlines()]
        print(count_increases_sliding(values, window=0))
        print(count_increases_sliding(values))


if __name__ == "__main__":
    main()
