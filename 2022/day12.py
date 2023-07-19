from typing import Iterable, Optional, Any, Self
from dataclasses import dataclass
from functools import total_ordering

alphabet = 'abcdefghijklmnopqrstuvwxyz'
height_map = {c: i for i, c in enumerate(alphabet)}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@total_ordering
class Distance:
    def __init__(self, d: int | str) -> None:
        if isinstance(d, int) or d == 'inf':
            self.d = d
        else:
             raise ValueError(f'd must be in or \'int\'. {d=}')

    def __eq__(self, other: "Distance") -> bool:
        return self.d == other.d

    def __lt__(self, other: "Distance") -> bool:
        if self.d == 'inf':
            return False
        if other.d == 'inf':
            return True
        return self.d < other.d
    
    def __add__(self, other: int | Self):
        if self.d == 'inf':
            return Distance('inf')
        if isinstance(other, int):
            return Distance(self.d + other)
        elif isinstance(other, Distance):
            if other.d == 'inf':
                return Distance('inf')
            else:
                return Distance(self.d + other.d)
        else:
            raise TypeError(f'Addition is not supported between Distance and {type(other)}.')
    
    def __str__(self) -> str:
        return str(self.d)
            
@dataclass
class Node:
    i: int
    j: int
    h: int
    c: str
    d: Distance
    visited: bool=False
    prev: "Node"=None

    @property
    def position(self) -> tuple[int, int]:
        return self.i, self.j
    
    @property
    def direction(self) -> str:
        if self.prev is None:
            return '.'
        i, j = self.position
        if i == self.prev.i + 1:
            return 'V'
        elif i == self.prev.i - 1:
            return '^'
        elif j == self.prev.j + 1:
            return '>'
        elif j == self.prev.j - 1:
            return '<'
        else:
            return 'X'
    
    def __str__(self) -> str:
        return f'Node(i={self.i}, j={self.j}, h={self.h}, d={self.d})'
    
class Grid:
    def __init__(self, height: int, width: int, fill: Any=None) -> None:
        self.height = height
        self.width = width
        self.shape = (height, width)
        self.fill = fill
        self.values: list[list[Any]] = [[fill for j in range(width)] for i in range(height)]
    
    def __getitem__(self, idx: tuple[int, int]):
        i, j = idx
        return self.values[i][j]
    
    def __setitem__(self, idx: tuple[int, int], value: Any):
        i, j = idx
        self.values[i][j] = value
    
    def __str__(self) -> str:
        lines = [''.join([str(item) for item in row]) + '\n' for row in self.values]
        return ''.join(lines)

    def iter(self):
        for i in range(self.height):
            for j in range(self.width):
                yield self.values[i][j]

    def print_path(self, end_node: Node) -> None:
        height_grid = [[alphabet[n.h] for n in row] + '\n' for row in self.values]


class Dijkstra:
    def __init__(self, path: str, reverse: bool=False) -> None:
        self.reverse = reverse
        self.load_map(path)

    def load_map(self, path: str, start: str='S', end: str='E'):
        with open(path) as f:
            lines = f.read().splitlines()

        height = len(lines)
        width = len(lines[0])
        self.grid = Grid(height, width)
        self.unvisited = []
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == start:
                    h = 0
                    d = Distance(0) if not self.reverse else Distance('inf')
                elif c == end:
                    h = 25
                    d = Distance('inf') if not self.reverse else Distance(0)
                else:
                    h = height_map[c]
                    d = Distance('inf')
                new_node = Node(i, j, h, c, d)
                self.unvisited.append(new_node)
                self.grid[i, j] = new_node
                if c == start:
                    self.start_node = new_node
                if c == end:
                    self.end_node = new_node
    
    def pop_unvisited(self) -> Node:
        min_index = 0
        min_distance = Distance('inf')
        for i, node in enumerate(self.unvisited):
            if node.d < min_distance:
                min_index = i
                min_distance = node.d
        return self.unvisited.pop(min_index)
    
    def valid_step(self, node_from: Node, node_to: Node) -> bool:
        if not self.reverse:
            return node_to.h - node_from.h <= 1
        return node_from.h - node_to.h <= 1

    def neighbors(self, node: Node) -> Iterable[Node]:
        i, j = node.position
        if i + 1 < self.grid.height and self.valid_step(node, self.grid[i+1,j]):
            yield self.grid[i+1,j]
        if j + 1 < self.grid.width and self.valid_step(node, self.grid[i,j+1]):
            yield self.grid[i,j+1]
        if i > 0 and self.valid_step(node, self.grid[i-1,j]):
            yield self.grid[i-1,j]
        if j > 0 and self.valid_step(node, self.grid[i,j-1]):
            yield self.grid[i,j-1]

    def solve(self):
        while len(self.unvisited) > 0:
            current_node = self.pop_unvisited()
            new_distance = current_node.d + 1
            for neighbor in self.neighbors(current_node):
                if neighbor.visited:
                    continue
                if new_distance < neighbor.d:
                    neighbor.d = new_distance
                    neighbor.prev = current_node
            current_node.visited = True
        self.print_grid()
        if not self.reverse:
            self.print_path(self.end_node)
        else:
            self.print_path(self.start_node)
    
    def find_min(self):
        min_distance = Distance('inf')
        min_node = None
        for node in self.grid.iter():
            if node.h != 0:
                continue
            if node.d < min_distance:
                print(node)
                min_distance = node.d
                min_node = node
        self.print_path(min_node)
        
    def print_path(self, node: Node):
        print_grid = Grid(self.grid.height, self.grid.width, fill='.')
        current_node = node
        while current_node.prev is not None:
            i, j = current_node.position
            c = current_node.direction
            print_grid[i,j] = f"{bcolors.FAIL}{c}{bcolors.ENDC}"
            current_node = current_node.prev
        print(print_grid)
        print(node.d)

    def print_grid(self):
        print_grid = Grid(self.grid.height, self.grid.width)
        for i in range(self.grid.height):
            for j  in range(self.grid.width):
                if self.grid[i,j] == self.end_node:
                    print_grid[i, j] = f"{bcolors.OKGREEN}E{bcolors.ENDC}"
                else:
                    print_grid[i, j] = self.grid[i,j].direction
        print(print_grid)
    
d = Dijkstra('day12-input', reverse=True)
d.solve()
d.find_min()