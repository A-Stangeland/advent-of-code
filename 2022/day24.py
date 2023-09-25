from aocd.models import Puzzle  # type: ignore
from math import lcm
from typing import Iterable

puzzle = Puzzle(year=2022, day=24)


class Valley:
    def __init__(self, data: str) -> None:
        lines = data.splitlines()
        self.height: int = len(lines) - 2
        self.width: int = len(lines[0]) - 2
        self.period: int = lcm(self.height, self.width)
        self._values: list[list[str]] = [
            [c for c in line[1:-1]] for line in lines[1:-1]
        ]
        self.start: tuple[int, int] = (-1, 0)
        self.end: tuple[int, int] = (self.height, self.width - 1)

    def isendpoint(self, i: int, j: int) -> bool:
        return (i, j) in [self.start, self.end]

    def isblocked(self, i: int, j: int, t: int) -> bool:
        if self.isendpoint(i, j):
            return False
        if self[(i + t) % self.height, j] == "^":
            return True
        if self[(i - t) % self.height, j] == "v":
            return True
        if self[i, (j + t) % self.width] == "<":
            return True
        if self[i, (j - t) % self.width] == ">":
            return True
        return False

    def isinbounds(self, i: int, j: int) -> bool:
        if self.isendpoint(i, j):
            return True
        return 0 <= i < self.height and 0 <= j < self.width

    def isvalid(self, i: int, j: int, t: int) -> bool:
        return self.isendpoint(i, j) or (
            self.isinbounds(i, j) and not self.isblocked(i, j, t)
        )

    def __getitem__(self, idx: tuple[int, int]) -> str:
        if not isinstance(idx, tuple):
            raise TypeError
        i, j = idx
        return self._values[i][j]

    def __str__(self) -> str:
        return "\n".join(["".join([c for c in line]) for line in self._values])


class FloodFill:
    def __init__(self, valley: Valley) -> None:
        self.valley = valley
        self.start: tuple[int, int] = (-1, 0)
        self.end = (valley.height, valley.width - 1)
        self.nodes: set[tuple[int, int]] = {self.start}
        self.t: int = 0

    def neighbors(self, node: tuple[int, int]) -> Iterable[tuple[int, int]]:
        i, j = node
        V = self.valley
        if V.isvalid(i, j, self.t + 1):
            yield i, j
        if V.isvalid(i + 1, j, self.t + 1):
            yield i + 1, j
        if V.isvalid(i, j + 1, self.t + 1):
            yield i, j + 1
        if V.isvalid(i - 1, j, self.t + 1):
            yield i - 1, j
        if V.isvalid(i, j - 1, self.t + 1):
            yield i, j - 1

    def step(self) -> None:
        new_nodes: set[tuple[int, int]] = set()
        for node in self.nodes:
            new_nodes.update(self.neighbors(node))
        self.nodes = new_nodes
        self.t += 1

    @property
    def complete(self) -> bool:
        return self.end in self.nodes

    def fill(self, display: bool = False) -> int:
        while not self.complete:
            self.step()
            if display:
                print(self.t)
                print(self)
        return self.t

    def roundtrip(self, display: bool = False) -> int:
        while self.end not in self.nodes:
            self.step()
        self.nodes = {self.end}
        while self.start not in self.nodes:
            self.step()
        self.nodes = {self.start}
        while self.end not in self.nodes:
            self.step()
        return self.t

    def __str__(self) -> str:
        lines = []
        for i in range(self.valley.height):
            line = []
            for j in range(self.valley.width):
                if self.valley.isblocked(i, j, self.t):
                    line.append("#")
                elif (i, j) in self.nodes:
                    line.append("O")
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)


def part1(data: str) -> int:
    valley = Valley(data)
    flood = FloodFill(valley)
    return flood.fill()


def part2(data: str) -> int:
    valley = Valley(data)
    flood = FloodFill(valley)
    return flood.roundtrip()


if __name__ == "__main__":
    print("--- Part 1 ---")
    print("Time to reach end:", part1(puzzle.input_data))
    print("--- Part 2 ---")
    print(
        "Time to go to end, go back to start, then back to end:",
        part2(puzzle.input_data),
    )
