import sys

def reduce_polymer(polymer, skip=None):
    result = []
    for ch in polymer:
        if skip is not None and ch.lower() == skip:
            continue
        if result and result[-1] != ch and result[-1].lower() == ch.lower():
            result.pop()
        else:
            result.append(ch)
    return ''.join(result)

def get_shortest_polymer_length(polymer):
    result = len(polymer)
    types = set(polymer.lower())
    for t in types:
        reduced_polymer = reduce_polymer(polymer, skip=t)
        result = min(result, len(reduced_polymer))

    return result


def main():
    polymer = sys.stdin.readline().strip()
    reduced_polymer = reduce_polymer(polymer)
    print(len(reduced_polymer))
    print(get_shortest_polymer_length(reduced_polymer))


if __name__ == '__main__':
    main()
