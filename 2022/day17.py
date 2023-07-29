from itertools import cycle

ROCKTYPES = ("-", "+", "L", "I", "o")


class Rock:
    def __init__(self, x: int, y: int, shape_id: str) -> None:
        assert shape_id in ROCKTYPES
        self.falling = True
        self.x = x
        self.y = y
        self.shape_id = shape_id
        self.shape = self.get_shape(shape_id)
        self.width = max(p[0] for p in self.shape) + 1
        self.height = max(p[1] for p in self.shape) + 1

    def get_shape(self, shape_id: str) -> set[tuple[int, int]]:
        match shape_id:
            case "-":
                return set([(0, 0), (1, 0), (2, 0), (3, 0)])
            case "+":
                return set([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)])
            case "L":
                return set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
            case "I":
                return set([(0, 0), (0, 1), (0, 2), (0, 3)])
            case "o":
                return set([(0, 0), (1, 0), (0, 1), (1, 1)])

    @property
    def origin(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def coordinates(self) -> set[tuple[int, int]]:
        ox, oy = self.origin
        return {(ox + sx, oy + sy) for sx, sy in self.shape}

    @property
    def xbounds(self) -> tuple[int, int]:
        ox = self.origin[0]
        return ox, ox + self.width

    @property
    def ybounds(self) -> tuple[int, int]:
        oy = self.origin[1]
        return oy, oy + self.height

    @property
    def lower_edge(self) -> set[tuple[int, int]]:
        return {
            min(filter(lambda p: p[0] == x, self.coordinates), key=lambda p: p[1])
            for x in range(*self.xbounds)
        }

    def move(self, jet: str, reverse=False) -> None:
        if jet == ">":
            if not reverse:
                self.right()
            else:
                self.left()
        elif jet == "<":
            if not reverse:
                self.left()
            else:
                self.right()

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def down(self):
        self.y -= 1

    def __repr__(self) -> str:
        return f"Rock(x={self.x}, y={self.y}, type={self.shape_id})"


class Tetris:
    def __init__(self, path: str) -> None:
        self.path = path
        with open(path) as f:
            data = f.read().strip()
        self.jetcycle_period = len(data)
        self.rockcycle_period = len(ROCKTYPES)
        self.jetcycle = cycle(enumerate(data))
        self.rockcycle = cycle(ROCKTYPES)
        self.width = 7
        self.tower: list[set[tuple[int, int]]] = []

    def __getitem__(self, idx: int | slice):
        if isinstance(idx, int):
            if idx >= self.tower_height:
                return set()
            return self.tower[idx]
        elif isinstance(idx, slice):
            start = idx.start if idx.start is not None else 0
            stop = idx.stop if idx.stop is not None else self.tower_height
            if start >= self.tower_height:
                return set()
            return set.union(*self.tower[start : min(stop, self.tower_height)])
        else:
            raise TypeError(f"Expected int or slice, got type {type(idx)}")

    def get_slice(self, start: int, stop: int) -> set[tuple[int, int]]:
        if start >= self.tower_height:
            return set()
        return set.union(*self.tower[start : min(stop, self.tower_height)])

    @property
    def tower_height(self) -> int:
        return len(self.tower)

    @property
    def spawn_point(self) -> tuple[int, int]:
        return 2, self.tower_height + 3

    def next_rock(self) -> Rock:
        return Rock(*self.spawn_point, next(self.rockcycle))

    def out_of_bounds(self, rock: Rock) -> bool:
        xmin, xmax = rock.xbounds
        return xmin < 0 or xmax > self.width

    def collision_check(self, rock: Rock) -> bool:
        lb, ub = rock.ybounds
        tower_coordinates = self.get_slice(lb, ub)
        return not rock.coordinates.isdisjoint(tower_coordinates)

    def stop_fall(self, rock: Rock) -> bool:
        for x, y in rock.lower_edge:
            if y == 0 or (x, y - 1) in self[y - 1]:
                return True
        return False

    def add_to_tower(self, rock: Rock) -> None:
        ymin, ymax = rock.ybounds
        while self.tower_height < ymax:
            self.tower.append(set())
        for x, y in rock.coordinates:
            self.tower[y].add((x, y))

    def add_rocks(self, n: int) -> None:
        for _ in range(n):
            rock = self.next_rock()
            for _, jet in self.jetcycle:
                rock.move(jet)
                if self.out_of_bounds(rock) or self.collision_check(rock):
                    rock.move(jet, reverse=True)
                if self.stop_fall(rock):
                    self.add_to_tower(rock)
                    break
                else:
                    rock.down()

    def height_after_n_rocks(self, n: int) -> None:
        cycle_elements = []
        cycle_heights = []
        last_rock_type = "o"
        last_jet_idx = self.jetcycle_period - 1
        delay_return = 10
        for i in range(n):
            if (last_jet_idx, last_rock_type) in cycle_elements:
                cycle_start = cycle_elements.index((last_jet_idx, last_rock_type))
                cycle_stop = len(cycle_elements)
                height_before_cycle = cycle_heights[cycle_start]
                height_after_cycle = self.tower_height
                cycle_height = height_after_cycle - height_before_cycle
                cycle_period = cycle_stop - cycle_start
                num_cycles, remainder = divmod(n - cycle_start, cycle_period)
                if delay_return == 0:
                    self.add_rocks(remainder)
                    remainder_height = self.tower_height - height_after_cycle
                    return (
                        height_before_cycle
                        + num_cycles * cycle_height
                        + remainder_height
                    )
                delay_return -= 1
            cycle_elements.append((last_jet_idx, last_rock_type))
            cycle_heights.append(self.tower_height)
            rock = self.next_rock()
            last_rock_type = rock.shape_id
            for jet_idx, jet in self.jetcycle:
                last_jet_idx = jet_idx
                rock.move(jet)
                if self.out_of_bounds(rock) or self.collision_check(rock):
                    rock.move(jet, reverse=True)
                if self.stop_fall(rock):
                    self.add_to_tower(rock)
                    break
                else:
                    rock.down()

    def head(self, n: int) -> None:
        lines = [
            "|"
            + "".join(
                ["#" if (x, y) in self.tower[y] else "." for x in range(self.width)]
            )
            + "|"
            for y in range(self.tower_height - n, self.tower_height)
        ]
        lines.insert(0, (self.width + 2) * "~")
        print("\n".join([line for line in lines[::-1]]))

    def __str__(self) -> str:
        lines = [
            "|"
            + "".join(
                ["#" if (x, y) in self.tower[y] else "." for x in range(self.width)]
            )
            + "|"
            for y in range(self.tower_height)
        ]
        lines.insert(0, "+" + self.width * "-" + "+")
        return "\n".join([line for line in lines[::-1]])

    def __repr__(self) -> str:
        lines = [
            "|"
            + "".join(
                ["#" if (x, y) in self.tower[y] else "." for x in range(self.width)]
            )
            + "|"
            for y in range(self.tower_height - 8, self.tower_height)
        ]
        lines.insert(0, (self.width + 2) * "~")
        return "\n".join([line for line in lines[::-1]])


def tower_height_after_n_rocks(jet_path: str, n: int) -> int:
    t = Tetris(jet_path)
    return t.add_rocks(n)


if __name__ == "__main__":
    # jet_path = "input.txt"
    jet_path = "day17-input"
    # ----- Part 1 -----
    h1 = tower_height_after_n_rocks(jet_path, 2022)
    print("Height of tower after 2022 rocks:", h1)

    # # ----- Part 2 -----
    h2 = tower_height_after_n_rocks(jet_path, 1_000_000_000_000)
    print("Height of tower after 1000000000000 rocks:", h2)
