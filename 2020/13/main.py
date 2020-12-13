from typing import List, NamedTuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

TEST_BUSES = '7,13,x,x,59,x,31,19'

def parse_busses(line):
    return [int(value) for value in line.split(',') if value != 'x']

ass([7, 13, 59, 31, 19], parse_busses, TEST_BUSES)

def parse_busses_with_positions(line):
    return [(idx, int(value)) for idx, value in enumerate(line.split(',')) if value != 'x']

def solve(depart_ts, buses):
    wait_time, bus = min((bus - depart_ts % bus, bus) for bus in buses)
    return wait_time * bus

ass(295, solve, 939, [7, 13, 59, 31, 19])

def cached(fun):
    cache = dict()
    def run(*args):
        key = args
        if key not in cache:
            cache[key] = fun(*args)
        return cache[key]
    return run

@cached
def find_inverse_by_modulo(a, m):
    return (a ** (m - 2)) % m

assert(find_inverse_by_modulo(7, 13) * 7 % 13 == 1)


def solve2(busses_with_positions):
    # So the values are actually primes,
    # so we can use Chinese remainder theorem.
    a = [(prime - rem) % prime for rem, prime in busses_with_positions]
    p = [prime for _, prime in busses_with_positions]
    x = deepcopy(a)
    for i, _ in enumerate(p):
        for j in range(0, i):
            x[i] = (x[i] - x[j]) * find_inverse_by_modulo(p[j], p[i]) % p[i]

    result = 0
    mult = 1
    for i, x in enumerate(x):
        result += x * mult
        mult *= p[i]

    return result

ass(3417, solve2, [(0, 17), (2, 13), (3, 19)])
ass(1068781, solve2, [(0, 7), (1, 13), (4, 59), (6, 31), (7, 19)])

    

def main():
    with open('in.txt') as infile:
        depart_ts = int(infile.readline().strip())
        bus_line = infile.readline().strip()
        buses = parse_busses(bus_line)
        print(solve(depart_ts, buses))
        print(solve2(parse_busses_with_positions(bus_line)))


if __name__ == "__main__":
    main()
