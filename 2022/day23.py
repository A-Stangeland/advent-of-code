from aocd.models import Puzzle  # type: ignore
from typing import Iterable, Optional

puzzle = Puzzle(year=2022, day=23)


class CellularSim:
    DIRECTIONS = ("N", "S", "W", "E")

    def __init__(self, data: str) -> None:
        self.coordinates = self.parse_elf_map(data)
        self.cycle_start = 0

    def parse_elf_map(self, data: str) -> set[tuple[int, int]]:
        coordinates = set()
        for i, line in enumerate(data.splitlines()):
            for j, c in enumerate(line):
                if c == "#":
                    coordinates.add((i, j))
        return coordinates

    def direction_cycle(self) -> Iterable[str]:
        for i in range(4):
            yield (self.DIRECTIONS[(self.cycle_start + i) % 4])

    def step_cycle(self, i: int, j: int) -> list[tuple[set[str], tuple[int, int]]]:
        return [
            ({"N", "W"}, (i - 1, j - 1)),
            ({"N"}, (i - 1, j)),
            ({"N", "E"}, (i - 1, j + 1)),
            ({"W"}, (i, j - 1)),
            ({"E"}, (i, j + 1)),
            ({"S", "W"}, (i + 1, j - 1)),
            ({"S"}, (i + 1, j)),
            ({"S", "E"}, (i + 1, j + 1)),
        ]

    def get_move_direction(self, coord: tuple[int, int]) -> Optional[str]:
        valid_directions = {"N", "S", "W", "E"}
        for d, x in self.step_cycle(*coord):
            if x in self.coordinates:
                valid_directions -= d
        if len(valid_directions) in (0, 4):
            return None
        for direction in self.direction_cycle():
            if direction in valid_directions:
                return direction
        return None

    def get_direction_coord(
        self, coord: tuple[int, int], direction: str
    ) -> tuple[int, int]:
        i, j = coord
        match direction:
            case "N":
                return i - 1, j
            case "S":
                return i + 1, j
            case "W":
                return i, j - 1
            case "E":
                return i, j + 1
            case _:
                raise ValueError(f"{direction} is not a valid direction.")

    def step(self) -> bool:
        move_proposals: dict[tuple[int, int], tuple[int, int]] = dict()
        blocked_coords: set = set()
        for coord in self.coordinates:
            direction = self.get_move_direction(coord)
            if direction is None:
                continue
            new_coord = self.get_direction_coord(coord, direction)
            if new_coord in move_proposals:
                blocked_coords.add(new_coord)
            else:
                move_proposals[new_coord] = coord

        if not move_proposals:
            return True

        for coord in blocked_coords:
            del move_proposals[coord]

        for destination, source in move_proposals.items():
            self.coordinates.remove(source)
            self.coordinates.add(destination)
        self.cycle_start = (self.cycle_start + 1) % 4
        return False

    def bounds(self) -> tuple[int, int, int, int]:
        i, j = next(iter(self.coordinates))
        imin, imax, jmin, jmax = i, i, j, j
        for i, j in self.coordinates:
            imin = min(imin, i)
            imax = max(imax, i)
            jmin = min(jmin, j)
            jmax = max(jmax, j)
        return imin, imax, jmin, jmax

    def empty_ground(self) -> int:
        imin, imax, jmin, jmax = self.bounds()
        return (imax - imin + 1) * (jmax - jmin + 1) - len(self.coordinates)

    def __str__(self) -> str:
        imin, imax, jmin, jmax = self.bounds()
        lines = []
        for i in range(imin - 1, imax + 2):
            line = []
            for j in range(jmin - 1, jmax + 2):
                c = "#" if (i, j) in self.coordinates else "."
                line.append(c)
            lines.append("".join(line))
        return "\n".join(lines)


def part1(data: str) -> int:
    sim = CellularSim(data)
    for i in range(10):
        sim.step()
    print(sim)
    return sim.empty_ground()


def part2(data: str) -> int:
    sim = CellularSim(data)
    i = 0
    stopped = False
    while not stopped:
        stopped = sim.step()
        i += 1
    print(sim)
    return i


if __name__ == "__main__":
    print("--- Part 1 ---")
    print("Empty ground:", part1(puzzle.input_data))
    print("--- Part 2 ---")
    print("First iteration without moves:", part2(puzzle.input_data))
