from aocd.models import Puzzle  # type: ignore

puzzle = Puzzle(year=2022, day=22)

DIRECTIONS = (">", "V", "<", "^")


class Manifold:
    def __init__(self, data: str, cube: bool, ignore_blocks: bool = False) -> None:
        self.cube = cube
        self.ignore_blocks = ignore_blocks
        map_data, move_data = data.split("\n\n")
        self.moves = move_data
        self.map = map_data.splitlines()
        self.height = len(self.map)
        self.width = max(len(row) for row in self.map)
        self.cube_size = self.height // 4
        self.i = 0
        self.j = self.map[self.i].index(".")
        self.d = 0
        self.path = {(self.i, self.j): self.d}
        self.left_edge = self.get_left_edge()
        self.right_edge = [len(row) - 1 for row in self.map]
        self.upper_edge = self.get_upper_edge()
        self.lower_edge = self.get_lower_edge()

    @property
    def direction(self):
        return DIRECTIONS[self.d]

    def get_left_edge(self):
        left_edge = []
        for row in self.map:
            j = row.index(".")
            try:
                j = min(j, row.index("#"))
            except ValueError:
                pass
            left_edge.append(j)
        return left_edge

    def get_upper_edge(self):
        upper_edge = []
        for j in range(self.width):
            for i in range(self.height):
                try:
                    if self.map[i][j] in [".", "#"]:
                        upper_edge.append(i)
                        break
                except IndexError:
                    pass
            else:
                raise ValueError(f"No upper edge found for column {j}.")
        return upper_edge

    def get_lower_edge(self):
        lower_edge = []
        for j in range(self.width):
            for i in reversed(range(self.height)):
                try:
                    if self.map[i][j] in [".", "#"]:
                        lower_edge.append(i)
                        break
                except IndexError:
                    pass
            else:
                raise ValueError(f"No lower edge found for column {j}.")
        return lower_edge

    def turn(self, direction: str):
        if direction == "R":
            self.d = (self.d + 1) % 4
        elif direction == "L":
            self.d = (self.d - 1) % 4
        self.path[self.i, self.j] = self.d

    def true_cube_position(self, i: int, j: int) -> tuple[int, int, int]:
        s = self.cube_size
        if i == -1 and s <= j < 2 * s:  # 1
            return 2 * s + j, 0, 0
        elif i == -1 and 2 * s <= j < 3 * s:  # 2
            return 4 * s - 1, j - 2 * s, 3
        elif i < s and j == 3 * s:  # 3
            return 3 * s - i - 1, 2 * s - 1, 2
        elif i == s and 2 * s <= j < 3 * s and self.d == 1:  # 4
            return j - s, 2 * s - 1, 2
        elif s <= i < 2 * s and j == 2 * s and self.d == 0:  # 4
            return s - 1, i + s, 3
        elif 2 * s <= i < 3 * s and j == 2 * s:  # 3
            return 3 * s - i - 1, 3 * s - 1, 2
        elif i == 3 * s and s <= j < 2 * s and self.d == 1:  # 5
            return j + 2 * s, s - 1, 2
        elif 3 * s <= i < 4 * s and j == s and self.d == 0:  # 5
            return 3 * s - 1, i - 2 * s, 3
        elif i == 4 * s and 0 <= j < s:  # 2
            return 0, j + 2 * s, 1
        elif 3 * s <= i < 4 * s and j == -1:  # 1
            return 0, i - 2 * s, 1
        elif 2 * s <= i < 3 * s and j == -1:  # 6
            return 3 * s - i - 1, s, 0
        elif i == 2 * s - 1 and 0 <= j < s and self.d == 3:  # 7
            return s + j, s, 0
        elif s <= i < 2 * s and j == s - 1 and self.d == 2:
            return 2 * s, i - s, 1
        elif 0 <= i < s and j == s - 1:  # 6
            return 3 * s - i - 1, 0, 0
        else:
            return i, j, self.d

    def next_position(self) -> tuple[int, int, int]:
        match self.direction:
            case ">":
                next_i = self.i
                next_j = self.j + 1
                if next_j > self.right_edge[self.i]:
                    next_j = self.left_edge[self.i]
            case "<":
                next_i = self.i
                next_j = self.j - 1
                if next_j < self.left_edge[self.i]:
                    next_j = self.right_edge[self.i]
            case "V":
                next_i = self.i + 1
                next_j = self.j
                if next_i > self.lower_edge[self.j]:
                    next_i = self.upper_edge[self.j]
            case "^":
                next_i = self.i - 1
                next_j = self.j
                if next_i < self.upper_edge[self.j]:
                    next_i = self.lower_edge[self.j]
            case _:
                raise ValueError(self.direction)
        return next_i, next_j, self.d

    def next_cube_position(self) -> tuple[int, int, int]:
        match self.direction:
            case ">":
                next_i = self.i
                next_j = self.j + 1
            case "<":
                next_i = self.i
                next_j = self.j - 1
            case "V":
                next_i = self.i + 1
                next_j = self.j
            case "^":
                next_i = self.i - 1
                next_j = self.j
            case _:
                raise ValueError(self.direction)
        return self.true_cube_position(next_i, next_j)

    def is_blocked(self, i, j) -> bool:
        return not self.ignore_blocks and self.map[i][j] == "#"

    def forward(self, n: int):
        for _ in range(n):
            next_i, next_j, next_d = (
                self.next_cube_position() if self.cube else self.next_position()
            )
            if self.is_blocked(next_i, next_j):
                break
            self.i = next_i
            self.j = next_j
            self.d = next_d
            self.path[self.i, self.j] = self.d

    def execute_moves(self):
        buffer = []
        for c in self.moves:
            if c.isnumeric():
                buffer.append(c)
            else:
                if buffer:
                    n = int("".join(buffer))
                    self.forward(n)
                    buffer = []
                self.turn(c)
        if buffer:
            n = int("".join(buffer))
            self.forward(n)
            buffer = []
        return 1000 * (self.i + 1) + 4 * (self.j + 1) + self.d

    def __str__(self) -> str:
        lines = [[c for c in row] for row in self.map]
        for (i, j), d in self.path.items():
            lines[i][j] = DIRECTIONS[d]
        return "\n".join(["".join(line) for line in lines])


def part1(data: str) -> str:
    m = Manifold(data, cube=False)
    password = m.execute_moves()
    # print(m)
    return password


def part2(data: str) -> str:
    m = Manifold(data, cube=True)
    password = m.execute_moves()
    # print(m)
    return password


if __name__ == "__main__":
    print("--- Part 1 ---")
    print("Password:", part1(puzzle.input_data))
    print("--- Part 2 ---")
    print("Password:", part2(puzzle.input_data))
