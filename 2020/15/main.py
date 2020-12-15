from typing import List, NamedTuple, Set
from enum import Enum
from collections import defaultdict
from copy import deepcopy
import tqdm

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def say_until(values, until, with_tqdm=False):
    last_value = values[-1]
    when_last_spoken = {value: turn for turn, value in enumerate(values[:-1])}

    iterations = range(len(values), until)
    if with_tqdm:
        iterations = tqdm.tqdm(iterations)
    for i in iterations:
        if last_value not in when_last_spoken:
            # It's the first time the number was spoken.
            prev_last_value, last_value = last_value, 0
        else:
            prev_last_value, last_value = last_value, i - 1 - when_last_spoken[last_value]
        when_last_spoken[prev_last_value] = i - 1

    return last_value

ass(436, say_until, [0, 3, 6], 2020)
ass(18, say_until, [3, 2, 1], 30000000)


def main():
    with open('in.txt') as infile:
        values = [int(value) for value in infile.readline().split(',')]
        print(say_until(values, 2020))
        print(say_until(values, 30000000, with_tqdm=True))


if __name__ == "__main__":
    main()
