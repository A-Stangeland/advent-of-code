from aocd.models import Puzzle  # type: ignore
from math import lcm
from dataclasses import dataclass

# from functools import total_ordering
from day12 import Distance, Grid
import heapq
from typing import Iterable

puzzle = Puzzle(year=2022, day=24)


@dataclass(order=True)
class Node:
    d: Distance
    i: int
    j: int
    visited: bool = False
    prev: "Node" = None

    @property
    def position(self) -> tuple[int, int]:
        return self.i, self.j

    def __repr__(self) -> str:
        return f"Node(i={self.i}, j={self.j}, d={self.d})"


class Map:
    def __init__(self, data: str) -> None:
        lines = data.splitlines()
        self.height: int = len(lines)
        self.width: int = len(lines[0])
        self.period: int = lcm(self.height - 2, self.width - 2)
        self._values: list[list[set[str]]] = [
            [{c} if c != "." else set() for c in line] for line in lines
        ]
        self.calculate_states()

    def calculate_states(self):
        self.states = []
        for _ in range(self.period):
            self.states.append(self._values)
            self.step()

    def step(self) -> None:
        new_values = [[set() for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if self.isblocked(i, j):
                    new_values[i][j].add("#")
                    continue
                cell = self._values[i][j]
                for item in cell:
                    match item:
                        case ">":
                            new_i = i
                            new_j = j + 1
                            if new_j == self.width - 1:
                                new_j = 1
                        case "<":
                            new_i = i
                            new_j = j - 1
                            if new_j == 0:
                                new_j = self.width - 2
                        case "v":
                            new_j = j
                            new_i = i + 1
                            if new_i == self.height - 1:
                                new_i = 1
                        case "^":
                            new_j = j
                            new_i = i - 1
                            if new_i == 0:
                                new_i = self.height - 2
                        case _:
                            raise ValueError(f"{i} {j} {item}")
                    new_values[new_i][new_j].add(item)
        self._values = new_values

    def isblocked(self, i: int, j: int) -> bool:
        cell = self._values[i][j]
        return len(cell) == 1 and next(iter(cell)) == "#"

    def __getitem__(self, idx: tuple[int, int]) -> set[str]:
        if not isinstance(idx, tuple):
            raise TypeError
        i, j = idx
        return self._values[i][j]

    def print_states(self):
        for n, values in enumerate(self.states):
            print(n + 1)
            print_lines = []
            for line in values:
                print_line = []
                for cell in line:
                    if len(cell) == 0:
                        print_line.append(".")
                    elif len(cell) == 1:
                        print_line.append(next(iter(cell)))
                    else:
                        print_line.append(str(len(cell))[0])
                print_lines.append("".join(print_line))
            print("\n".join(print_lines))

    def __str__(self) -> str:
        print_lines = []
        for line in self._values:
            print_line = []
            for cell in line:
                if len(cell) == 0:
                    print_line.append(".")
                elif len(cell) == 1:
                    print_line.append(next(iter(cell)))
                else:
                    print_line.append(str(len(cell))[0])
            print_lines.append("".join(print_line))
        return "\n".join(print_lines)


class Valley:
    def __init__(self, data: str) -> None:
        lines = data.splitlines()
        self.height: int = len(lines) - 2
        self.width: int = len(lines[0]) - 2
        self.period: int = lcm(self.height, self.width)
        self._values: list[list[str]] = [
            [c for c in line[1:-1]] for line in lines[1:-1]
        ]

    def isblocked(self, i: int, j: int, t: int) -> bool:
        if self[(i + t) % self.height, j] == "^":
            return True
        if self[(i - t) % self.height, j] == "v":
            return True
        if self[i, (j + t) % self.width] == "<":
            return True
        if self[i, (j - t) % self.width] == ">":
            return True
        return False

    def __getitem__(self, idx: tuple[int, int]) -> set[str]:
        if not isinstance(idx, tuple):
            raise TypeError
        i, j = idx
        return self._values[i][j]

    def __str__(self) -> str:
        return "\n".join(["".join([c for c in line]) for line in self._values])


class Astar:
    def __init__(self, valley: Valley) -> None:
        self.valley = valley
        self.start = (-1, 0)
        self.end = (valley.height - 1, valley.width - 1)
        # self.paths = [(0, self.start)]
        self.grid = Grid(valley.height, valley.width)
        self.unvisited = [Node(Distance(0), *self.start)]
        for i in range(valley.height):
            for j in range(valley.width):
                new_node = Node(Distance("inf"), i, j)
                self.grid[i, j] = new_node
                self.unvisited.append(new_node)

    def neighbors(self, node: Node) -> Iterable[Node]:
        i, j = node.position
        t = int(node.d)
        V = self.valley
        if i + 1 < V.height and not V.isblocked(i + 1, j, t + 1):
            yield self.grid[i + 1, j]
        if j + 1 < V.width and not V.isblocked(i, j + 1, t + 1):
            yield self.grid[i, j + 1]
        if i > 0 and not V.isblocked(i - 1, j, t + 1):
            yield self.grid[i - 1, j]
        if j > 0 and not V.isblocked(i, j - 1, t + 1):
            yield self.grid[i, j - 1]

    def step(self):
        while self.unvisited:
            current_node = heapq.heappop(self.unvisited)
            print(current_node)
            print(current_node.position == self.end)
            self.print_grid(current_node)
            if current_node.position == self.end:
                self.print_path(current_node)
                return
            new_distance = current_node.d + 1
            all_neighbors_visited = True
            for neighbor in self.neighbors(current_node):
                if neighbor.visited:
                    continue
                all_neighbors_visited = False
                if new_distance < neighbor.d:
                    neighbor.d = new_distance
                    neighbor.prev = current_node

            i, j = current_node.position
            t = int(current_node.d)
            if all_neighbors_visited or self.valley.isblocked(i, j, t + 1):
                current_node.visited = True
            else:
                heapq.heappush(self.unvisited, Node(Distance(t + 1), i, j))

    def print_path(self, node: Node):
        print_grid = Grid(self.grid.height, self.grid.width, fill=".")
        current_node = node
        while current_node.prev is not None:
            print(current_node)
            i, j = current_node.position
            print_grid[i, j] = "#"
            current_node = current_node.prev
        print(print_grid)
        print(node.d)

    def print_grid(self, current_node: Node):
        print_grid = Grid(self.grid.height, self.grid.width, fill=" .")
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                if current_node.position == (i, j):
                    print_grid[i, j] = "XX"
                elif self.grid[i, j].visited:
                    print_grid[i, j] = f"{str(self.grid[i, j].d):>2}"
        print(print_grid)


def part1(data: str) -> str:
    pass


def part2(data: str) -> str:
    pass


if __name__ == "__main__":
    with open("input.txt") as f:
        valley = Valley(f.read())
    # valley = Valley(puzzle.examples[0].input_data)
    # valley = Valley(puzzle.input_data)
    astar = Astar(valley)
    print(astar.unvisited)
    astar.step()
