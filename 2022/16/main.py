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
    rate: int
    connected_valves: List[str]


VALVE = "Valve "
RATE_PREFIX = "Valve AA has flow rate="
CONNECTED_VALVES_PREFIX = " tunnels lead to valves "


def parse_connected_valves(valve_str: str) -> List[str]:
    if "valves" in valve_str:
        return valve_str[len(CONNECTED_VALVES_PREFIX) :].split(", ")
    return [valve_str.split()[-1]]


def parse_valve(line: str) -> Tuple[str, Valve]:
    name = line[len(VALVE) : len(VALVE) + 2]
    rate_part, rest = line.split(";")
    rate = int(rate_part[len(RATE_PREFIX) :])
    connected_valves = parse_connected_valves(rest)
    return name, Valve(rate=rate, connected_valves=connected_valves)


def parse(lines: List[str]) -> Dict[str, Valve]:
    result = dict()
    for line in lines:
        name, valve = parse_valve(line)
        result[name] = valve

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


assrt(("BB", Valve(rate=13, connected_valves=["CC", "AA"])), parse_valve, TEST_DATA[1])
assrt(("JJ", Valve(rate=21, connected_valves=["II"])), parse_valve, TEST_DATA[-1])


class SimpleValve(NamedTuple):
    rate: int
    # Cost in time to get to the next valve.
    connected_valves: Dict[str, int]


# Removes all the valves which have rate 0 (except AA) by removing their node and replacing it with a longer edge to their children.
def simplify_valves(valves: Dict[str, Valve]) -> Dict[str, SimpleValve]:
    new_valves: Dict[str, Dict[str, int]] = {
        name: {s: 1 for s in valve.connected_valves} for name, valve in valves.items()
    }

    removed_valves: Set[str] = set(["AA"])
    removed = True
    while removed:
        removed = False
        for name_to_remove, valve_to_remove in valves.items():
            if name_to_remove not in removed_valves and valve_to_remove.rate == 0:
                removed_valves.add(name_to_remove)
                removed = True

                new_new_valves: Dict[str, Dict[str, int]] = dict()
                for name, children in new_valves.items():
                    if name_to_remove != name:
                        new_children = dict()
                        for child, cost in children.items():
                            if child == name_to_remove:
                                for next_child, child_cost in new_valves[child].items():
                                    if next_child != name:
                                        new_children[next_child] = cost + child_cost
                            else:
                                new_children[child] = cost
                        new_new_valves[name] = new_children

                assert len(new_new_valves) < len(new_valves)
                new_valves = new_new_valves

    return {
        name: SimpleValve(rate=valves[name].rate, connected_valves=ch)
        for name, ch in new_valves.items()
    }


assrt(
    {
        "AA": SimpleValve(rate=0, connected_valves={"BB": 1, "CC": 2}),
        "BB": SimpleValve(rate=2, connected_valves={"CC": 2}),
        "CC": SimpleValve(rate=3, connected_valves={"AA": 1}),
    },
    simplify_valves,
    {
        "AA": Valve(rate=0, connected_valves=["BB", "DD"]),
        "BB": Valve(rate=2, connected_valves=["DD"]),
        "CC": Valve(rate=3, connected_valves=["AA"]),
        "DD": Valve(rate=0, connected_valves=["CC"]),
    },
)


def go_maker(
    valves: Dict[str, SimpleValve],
    open_valves: Set[str],
    cache: Dict[Tuple[str, int, FrozenSet[str]], int],
):
    def go(
        current: str,
        time_remaining: int,
    ) -> int:
        key = (current, time_remaining, frozenset(open_valves))
        if key not in cache:
            valve = valves[current]
            result = 0
            if time_remaining > 0:
                if current not in open_valves:
                    open_valves.add(current)
                    result = (time_remaining - 1) * valve.rate + go(
                        current, time_remaining - 1
                    )
                    open_valves.remove(current)

                for next_valve, cost in valve.connected_valves.items():
                    if time_remaining > cost:
                        result = max(result, go(next_valve, time_remaining - cost))

            cache[key] = result

        return cache[key]

    return go


def solve1(lines: List[str]) -> int:
    valves = simplify_valves(parse(lines))

    cache: Dict[Tuple[str, int, FrozenSet[str]], int] = dict()
    open_valves: Set[str] = set("AA")
    return go_maker(valves, open_valves, cache)("AA", 30)


assrt(1651, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    valves = simplify_valves(parse(lines))

    cache: Dict[Tuple[str, int, FrozenSet[str]], int] = dict()
    second_cache: Dict[Tuple[str, int, FrozenSet[str]], Tuple[int, int]] = dict()
    open_valves: Set[str] = set("AA")

    go = go_maker(valves, open_valves, cache)

    def over_go(current: str, time_remaining: int) -> Tuple[int, int]:
        key = (current, time_remaining, frozenset(open_valves))
        if key not in second_cache:
            valve = valves[current]
            result = 0
            elephant_score = go("AA", 26)
            for next_valve, cost in valve.connected_valves.items():
                if time_remaining > cost:
                    next_result, next_elephant_score = over_go(
                        next_valve, time_remaining - cost
                    )
                    if result + elephant_score < next_result + next_elephant_score:
                        result = next_result
                        elephant_score = next_elephant_score

            if time_remaining > 0:
                if current not in open_valves:
                    open_valves.add(current)
                    open_result, open_elephant_score = over_go(
                        current, time_remaining - 1
                    )
                    open_result += (time_remaining - 1) * valve.rate
                    if open_result + open_elephant_score > result + elephant_score:
                        result = open_result
                        elephant_score = open_elephant_score
                    open_valves.remove(current)

            second_cache[key] = (result, elephant_score)

        return second_cache[key]

    return sum(over_go("AA", 26))


assrt(1707, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
