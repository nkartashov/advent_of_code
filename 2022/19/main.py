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
from itertools import product, combinations, chain
import traceback
import tqdm
import math

from copy import deepcopy


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")


Cost = List[int]

MATERIALS = ["ore", "clay", "obsidian", "geode"]
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


class Blueprint(NamedTuple):
    idx: int
    costs: List[Cost]

    def build(self, idx: int, resources: List[int]) -> List[int]:
        remaining_resources = [
            res - cost
            for res, cost in zip(resources, self.costs[idx])
            if res - cost >= 0
        ]
        if len(remaining_resources) == len(self.costs[idx]):
            return remaining_resources

        assert False

    # Returns amount of time to wait until a robot it buildable.
    def how_long_until_can_build(
        self, idx: int, resources: List[int], robots: List[int]
    ) -> Optional[int]:
        result = 0
        for (res, cost), rob in zip(zip(resources, self.costs[idx]), robots):
            if rob == 0:
                if cost > res:
                    return None
                else:
                    continue

            result = max(result, math.ceil(max(0, cost - res) / rob))
        return result


TEST_DATA = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".split(
    "\n"
)

COSTS = "costs "


def parse_cost_string(cost_string: str) -> Cost:
    cost_idx = cost_string.index(COSTS)
    parts = cost_string[cost_idx + len(COSTS) :].split()
    result = []
    for material in MATERIALS:
        material_idx = None
        try:
            material_idx = parts.index(material)
        except ValueError:
            pass
        result.append(int(parts[material_idx - 1]) if material_idx is not None else 0)

    return result


assrt([3, 0, 12, 0], parse_cost_string, "Each geode robot costs 3 ore and 12 obsidian")


def parse_blueprint(line: str) -> Blueprint:
    left, right = line.split(":")
    # Last full stop generates an empty string.
    cost_strings = right.split(".")[:-1]
    return Blueprint(
        idx=int(left.split()[-1]), costs=[parse_cost_string(s) for s in cost_strings]
    )


assrt(
    Blueprint(idx=2, costs=[[2, 0, 0, 0], [3, 0, 0, 0], [3, 8, 0, 0], [3, 0, 12, 0]]),
    parse_blueprint,
    TEST_DATA[1],
)


def parse_blueprints(lines: List[str]) -> List[Blueprint]:
    result = []
    for line in lines:
        result.append(parse_blueprint(line))

    return result


def robot_tick(time_left: int, resources: List[int], robots: List[int]) -> List[int]:
    return [res + rob * time_left for res, rob in zip(resources, robots)]


def add_robot(idx: int, robots: List[int]) -> List[int]:
    return [c + 1 if i == idx else c for i, c in enumerate(robots)]


MAX_CYCLES = 24 * 100


def cycles_to_fulfill(costs: List[int], robots: List[int]) -> List[int]:
    result = []
    for cost, robot in zip(costs, robots):
        if cost == 0:
            result.append(0)
            continue

        result.append(math.ceil(cost / robot) if robot != 0 else MAX_CYCLES)

    return result


def optimize_geode(blueprint: Blueprint, time_left: int) -> int:
    resources = [0, 0, 0, 0]
    robots = [1, 0, 0, 0]

    def make_robot(
        idx: int, time_left: int, resources: List[int], robots: List[int]
    ) -> Tuple[int, List[int], List[int]]:
        time_to_wait = blueprint.how_long_until_can_build(idx, resources, robots)
        assert time_to_wait is not None and time_to_wait >= 0

        resources = robot_tick(time_to_wait + 1, resources, robots)
        resources = blueprint.build(idx, resources)
        time_left -= time_to_wait + 1
        robots = add_robot(idx, robots)
        return time_left, resources, robots

    def get_times_to_build(
        resources: List[int], robots: List[int]
    ) -> List[Optional[int]]:
        result = []
        for i in range(len(robots)):
            result.append(blueprint.how_long_until_can_build(i, resources, robots))
        return result

    MAX_ORE_COUNT = 10

    def go(time_left: int, resources: List[int], robots: List[int]) -> int:
        ore, clay, obsidian, geode = get_times_to_build(resources, robots)

        assert clay is not None
        assert ore is not None

        result = 0
        if geode is not None and geode < time_left:
            new_time_left, new_resources, new_robots = make_robot(
                GEODE, time_left, resources, robots
            )
            result = new_time_left + go(new_time_left, new_resources, new_robots)

        if obsidian is not None and obsidian < time_left:
            new_time_left, new_resources, new_robots = make_robot(
                OBSIDIAN, time_left, resources, robots
            )
            result = max(result, go(new_time_left, new_resources, new_robots))

        if clay < time_left:
            new_time_left, new_resources, new_robots = make_robot(
                CLAY, time_left, resources, robots
            )
            result = max(result, go(new_time_left, new_resources, new_robots))

        if obsidian is None:
            if robots[ORE] < MAX_ORE_COUNT:
                new_time_left, new_resources, new_robots = make_robot(
                    ORE, time_left, resources, robots
                )
                result = max(result, go(new_time_left, new_resources, new_robots))

        return result

    return go(time_left, resources, robots)


def solve1(lines: List[str], minutes: int = 24) -> int:
    result = 0
    blueprints = parse_blueprints(lines)
    for blueprint in tqdm.tqdm(blueprints):
        result += blueprint.idx * optimize_geode(blueprint, minutes)
    return result


assrt(9, optimize_geode, parse_blueprints(TEST_DATA)[0], 24)
assrt(33, solve1, TEST_DATA)


def solve2(lines: List[str]) -> int:
    pass


assrt(58, solve2, TEST_DATA)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
