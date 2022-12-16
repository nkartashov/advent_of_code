from typing import (
    List,
    NamedTuple,
    Tuple,
    Dict,
    Union,
    Deque,
    Set,
    Optional,
    Iterable,
    FrozenSet,
)
from enum import Enum
from collections import deque
from itertools import product, combinations
import traceback

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")


class Valve(NamedTuple):
    name: str
    rate: int
    connected_valves: List[str]


VALVE = "Valve "
RATE_PREFIX = "Valve AA has flow rate="
CONNECTED_VALVES_PREFIX = " tunnels lead to valves "


def parse_connected_valves(valve_str: str) -> List[str]:
    if "valves" in valve_str:
        return valve_str[len(CONNECTED_VALVES_PREFIX) :].split(", ")
    return [valve_str.split()[-1]]


def parse_valve(line: str) -> Valve:
    name = line[len(VALVE) : len(VALVE) + 2]
    rate_part, rest = line.split(";")
    rate = int(rate_part[len(RATE_PREFIX) :])
    connected_valves = parse_connected_valves(rest)
    return Valve(name=name, rate=rate, connected_valves=connected_valves)


def parse(lines: List[str]) -> Dict[str, Valve]:
    result = dict()
    for line in lines:
        valve = parse_valve(line)
        result[valve.name] = valve

    return result


TEST_DATA = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".split(
    "\n"
)


assrt(
    Valve(name="BB", rate=13, connected_valves=["CC", "AA"]), parse_valve, TEST_DATA[1]
)
assrt(Valve(name="JJ", rate=21, connected_valves=["II"]), parse_valve, TEST_DATA[-1])


def solve1(lines: List[str]) -> int:
    valves = parse(lines)

    cache: Dict[Tuple[int, str, FrozenSet[str]], int] = dict()
    open_valves: Set[str] = set("AA")

    def go(
        current: str,
        time_remaining: int,
    ) -> int:
        key = (time_remaining, current, frozenset(open_valves))
        if key not in cache:
            valve = valves[current]
            result = 0
            if time_remaining > 0:
                if current not in open_valves and valve.rate > 0:
                    open_valves.add(current)
                    r1 = (time_remaining - 1) * valve.rate

                    if (time_remaining - 1) > 1:
                        for next_valve in valve.connected_valves:
                            result = max(
                                result, r1 + go(next_valve, time_remaining - 2)
                            )
                    open_valves.remove(current)

                for next_valve in valve.connected_valves:
                    result = max(result, go(next_valve, time_remaining - 1))

            cache[key] = result

        return cache[key]

    current = "AA"
    time_remaining = 30
    return go(current, time_remaining)


assrt(1651, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    pass


assrt(56000011, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
