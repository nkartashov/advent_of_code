import sys
from collections import Counter

def read_all_ids():
    return [line.strip() for line in sys.stdin]

def find_common_characters(s1, s2):
    return ''.join(ch1 for ch1, ch2 in zip(s1, s2) if ch1 == ch2)

def get_common_characters_for_set(s, ids):
    for id in ids:
        common = find_common_characters(s, id)
        if len(common) == len(s) - 1:
            return common
    return None


def main():
    twos = 0
    threes = 0
    ids = read_all_ids()
    common_result = None
    for line in ids:
        counts = Counter(line.strip())
        if any(c == 2 for _, c in counts.items()):
            twos += 1
        if any(c == 3 for _, c in counts.items()):
            threes += 1
        test_common = get_common_characters_for_set(line, ids)
        if test_common is not None:
            common_result = test_common
    print(twos * threes)
    print(common_result)

if __name__ == '__main__':
    main()
