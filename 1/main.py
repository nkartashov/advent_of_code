import sys

def read_all_frequencies():
    return [int(line.strip()) for line in sys.stdin]


def main():
    freqs = read_all_frequencies()
    current = 0
    seen = set([current])
    i = 0
    while True:
        current += freqs[i % len(freqs)]
        if current in seen:
            break
        seen.add(current)
        i += 1

    print(sum(freqs))
    print(current)

if __name__ == '__main__':
    main()
