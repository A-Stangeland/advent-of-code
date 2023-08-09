from aocd.models import Puzzle  # type: ignore
from copy import deepcopy
import re
import math
from math import ceil


puzzle = Puzzle(year=2022, day=19)

ROBOT_TYPES = ("ore", "clay", "obsidian", "geode")
ROBOT_TYPE_SHORT = {"ore": "o", "clay": "c", "obsidian": "b", "geode": "g"}


class TooExpensiveError(Exception):
    pass


class RobotFactory:
    def __init__(self, robot_cost: dict[str, dict[str, int]]) -> None:
        self.robot_cost = robot_cost
        self.resource_pool: dict[str, int] = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        }
        self.production: dict[str, int] = {
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        }

    def produce(self, t: int = 1):
        for resource, output in self.production.items():
            self.resource_pool[resource] += output * t

    def can_afford(self, robot_type: str) -> bool:
        for resource, cost in self.robot_cost[robot_type].items():
            if self.resource_pool[resource] < cost:
                return False
        return True

    def production_imbalance(self, robot_type: str) -> bool:
        if robot_type == "clay":
            max_clay_ratio = (
                self.robot_cost["obsidian"]["clay"] / self.robot_cost["obsidian"]["ore"]
            )
            if self.production["clay"] / self.production["ore"] > max_clay_ratio:
                return True
        elif robot_type == "obsidian":
            max_obsidian_ratio = (
                self.robot_cost["geode"]["obsidian"] / self.robot_cost["geode"]["ore"]
            )
            if (
                self.production["obsidian"] / self.production["ore"]
                > max_obsidian_ratio
            ):
                return True
        return False

    def time_to_produce(self, robot_type: str) -> float:
        return 1 + max(
            max(0, cost - self.resource_pool[resource]) / self.production[resource]
            if self.production[resource] > 0
            else math.inf
            for resource, cost in self.robot_cost[robot_type].items()
        )

    def build_robot(self, robot_type: str):
        if not self.can_afford(robot_type):
            raise TooExpensiveError()
        for resource, cost in self.robot_cost[robot_type].items():
            self.resource_pool[resource] -= cost
        self.produce(1)
        self.production[robot_type] += 1

    def __str__(self) -> str:
        lines = []
        for robot_type in ROBOT_TYPES:
            if not self.production[robot_type]:
                continue
            lines.append(
                f"{self.production[robot_type]} {robot_type}-collecting robot "
                f"collects {self.production[robot_type]} {robot_type}; "
                f"you now have {self.resource_pool[robot_type]} {robot_type}."
            )
        return "\n".join(lines)

    def __deepcopy__(self, memo) -> "RobotFactory":
        new_factory = RobotFactory(self.robot_cost)
        new_factory.resource_pool = deepcopy(self.resource_pool)
        new_factory.production = deepcopy(self.production)
        return new_factory


def parse_blueprint(blueprint: str) -> tuple[int, dict[str, dict[str, int]]]:
    id_number: int = int(re.findall(r"Blueprint (\d+)", blueprint)[0])
    ore_robot_cost: dict[str, int] = {
        "ore": int(re.findall(r"Each ore robot costs (\d+)", blueprint)[0])
    }
    clay_robot_cost: dict[str, int] = {
        "ore": int(re.findall(r"Each clay robot costs (\d+)", blueprint)[0])
    }
    obsidian_robot_cost: dict[str, int] = {
        "ore": int(re.findall(r"Each obsidian robot costs (\d+)", blueprint)[0]),
        "clay": int(
            re.findall(r"Each obsidian robot costs \d+ ore and (\d+)", blueprint)[0]
        ),
    }
    geode_robot_cost: dict[str, int] = {
        "ore": int(re.findall(r"Each geode robot costs (\d+)", blueprint)[0]),
        "obsidian": int(
            re.findall(r"Each geode robot costs \d+ ore and (\d+)", blueprint)[0]
        ),
    }
    robot_cost = {
        "ore": ore_robot_cost,
        "clay": clay_robot_cost,
        "obsidian": obsidian_robot_cost,
        "geode": geode_robot_cost,
    }
    return id_number, robot_cost


def triangle_number(n: int) -> int:
    return (n * (n + 1)) // 2


def geode_upper_bound(factory: RobotFactory, time_left: int) -> int:
    return (
        factory.resource_pool["geode"]
        + factory.production["geode"] * time_left
        + triangle_number(time_left - 1)
    )


class GeodeOptimizer:
    def __init__(self, time_limit: int) -> None:
        self.time_limit = time_limit

    def max_geode_production_recur(
        self, factory: RobotFactory, time_left: int, build_order: str
    ) -> int:
        if time_left == 0:
            if factory.resource_pool["geode"] > self.current_max:
                # print("------------")
                # print(build_order)
                # print(factory.production)
                # print(factory.resource_pool)
                self.current_max = factory.resource_pool["geode"]
            return factory.resource_pool["geode"]
        if geode_upper_bound(factory, time_left) < self.current_max:
            return 0
        outcomes: set[int] = set()
        wait_for_end_checked = False
        for robot_type in reversed(ROBOT_TYPES):
            t = factory.time_to_produce(robot_type)
            if math.isinf(t):
                continue
            t = ceil(t)
            new_factory = deepcopy(factory)
            if t >= time_left:
                if wait_for_end_checked:
                    continue
                new_factory.produce(time_left)
                new_build = build_order + "w" * time_left
                outcomes.add(self.max_geode_production_recur(new_factory, 0, new_build))
                wait_for_end_checked = True
            else:
                new_factory.produce(t - 1)
                new_factory.build_robot(robot_type)
                new_build = build_order + "w" * (t - 1) + ROBOT_TYPE_SHORT[robot_type]
                outcomes.add(
                    self.max_geode_production_recur(
                        new_factory, time_left - t, new_build
                    )
                )
        return max(outcomes)

    def max_geode_production(self, blueprint):
        id_number, robot_cost = parse_blueprint(blueprint)
        factory = RobotFactory(robot_cost)
        self.current_max = 0
        geode_production = self.max_geode_production_recur(factory, self.time_limit, "")
        print(id_number, geode_production)
        return geode_production

    def quality_level(self, blueprint: str):
        id_number, robot_cost = parse_blueprint(blueprint)
        factory = RobotFactory(robot_cost)
        self.current_max = 0
        geode_production = self.max_geode_production_recur(factory, self.time_limit, "")
        print(id_number, geode_production, id_number * geode_production)
        return id_number * geode_production


def test_factory(blueprint: str):
    id_number, robot_cost = parse_blueprint(blueprint)
    factory = RobotFactory(robot_cost)
    build_order = "wwcwcwcwwwbcwwbwwgwwgwww"
    # build_order = "wwwowococccccbcbbgbgbggw"
    for t, c in enumerate(build_order):
        print(f"\n== Mininute {t+1} ==")
        match c:
            case "o":
                factory.build_robot("ore")
                print("Build ore robot")
            case "c":
                factory.build_robot("clay")
                print("Build clay robot")
            case "b":
                factory.build_robot("obsidian")
                print("Build obsidian robot")
            case "g":
                factory.build_robot("geode")
                print("Build geode robot")
            case "w":
                factory.produce(1)
        print(factory)


def part1(data: str) -> str:
    g = GeodeOptimizer(24)
    return sum(g.quality_level(blueprint) for blueprint in data.splitlines())


def part2(data: str) -> str:
    g = GeodeOptimizer(32)
    return math.prod(
        g.max_geode_production(blueprint) for blueprint in data.splitlines()[:3]
    )


if __name__ == "__main__":
    print("--- Part 1 ---")
    print("Sum of quality numbers:", part1(puzzle.input_data))
    print("--- Part 2 ---")
    print("Product of first three blueprints:", part2(puzzle.input_data))
