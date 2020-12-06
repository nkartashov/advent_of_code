from typing import List, NamedTuple
from collections import Counter

def split_lines_into_groups(lines):
    result = []
    current_group = []
    for line in lines:
        if not line:
            result.append(current_group)
            current_group = []
        else:
            current_group.append(line)
    if current_group:
        result.append(current_group)
    return result

def count_group_answer(group) -> int:
    result_counter = Counter()
    for line in group:
        result_counter.update(line)
    return len(result_counter)

def count_group_answer_intersection(group) -> int:
    return len(set.intersection(*(set(line) for line in group)))


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        groups = split_lines_into_groups(lines)
        print(sum(count_group_answer(group) for group in groups))
        print(sum(count_group_answer_intersection(group) for group in groups))


if __name__ == "__main__":
    main()
