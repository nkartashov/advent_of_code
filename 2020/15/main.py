from typing import List, NamedTuple, Set
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def say_until(values, until):
    last_value = values[-1]
    when_last_spoken = defaultdict(list, {value: [turn] for turn, value in enumerate(values)})
    for i in range(len(values), until):
        if len(when_last_spoken[last_value]) == 1:
            # It's the first time the number was spoken.
            last_value = 0
        else:
            last_value = i - 1 - when_last_spoken[last_value][-2]
        when_last_spoken[last_value].append(i)
    return last_value

ass(436, say_until, [0, 3, 6], 2020)


def main():
    with open('in.txt') as infile:
        values = [int(value) for value in infile.readline().split(',')]
        print(say_until(values, 2020))


if __name__ == "__main__":
    main()
