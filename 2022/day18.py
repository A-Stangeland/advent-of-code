from aocd import get_data
from typing import Iterable

Point = tuple[int, int, int]


def load_points() -> set[Point]:
    data = get_data(day=18, year=2022)
    points = {tuple(int(x) for x in line.split(",")) for line in data.splitlines()}
    return points


def num_exposed_faces(points: set[Point]) -> int:
    n = len(points) * 6
    n_adjacent = 2 * (
        sum(int((x - 1, y, z) in points) for (x, y, z) in points)
        + sum(int((x, y - 1, z) in points) for (x, y, z) in points)
        + sum(int((x, y, z - 1) in points) for (x, y, z) in points)
    )
    return n - n_adjacent


class LavaDroplet:
    def __init__(self) -> None:
        self.droplet = load_points()
        self.set_bounds(pad=1)
        self.steam: set[Point] = set()
        self.steam_source: Point = (0, 0, 0)

    def set_bounds(self, pad: int) -> None:
        self.xmin: int = min(x for (x, _, _) in self.droplet) - pad
        self.xmax: int = max(x for (x, _, _) in self.droplet) + pad
        self.ymin: int = min(y for (_, y, _) in self.droplet) - pad
        self.ymax: int = max(y for (_, y, _) in self.droplet) + pad
        self.zmin: int = min(z for (_, _, z) in self.droplet) - pad
        self.zmax: int = max(z for (_, _, z) in self.droplet) + pad

    def out_of_bounds(self, point: set[Point]) -> bool:
        x, y, z = point
        if x < self.xmin or x > self.xmax:
            return True
        if y < self.ymin or y > self.ymax:
            return True
        if z < self.zmin or z > self.zmax:
            return True
        return False

    def neighbors(self, point: set[Point]) -> Iterable[Point]:
        x, y, z = point
        yield x - 1, y, z
        yield x + 1, y, z
        yield x, y - 1, z
        yield x, y + 1, z
        yield x, y, z - 1
        yield x, y, z + 1

    def exterior_surface(self) -> int:
        exterior_faces = 0
        point_queue = [self.steam_source]
        while point_queue:
            point = point_queue.pop(0)
            if self.out_of_bounds(point):
                continue
            if point in self.steam:
                continue
            if point in self.droplet:
                exterior_faces += 1
                continue
            self.steam.add(point)
            point_queue.extend(self.neighbors(point))
        return exterior_faces

    def __str__(self) -> str:
        layers = []
        for z in range(self.zmin, self.zmax + 1):
            lines = []
            for y in range(self.ymin, self.ymax + 1):
                line = []
                for x in range(self.xmin, self.xmax + 1):
                    c = "."
                    if (x, y, z) in self.droplet:
                        c = "#"
                    if (x, y, z) in self.steam:
                        c = "~"
                    line.append(c)
                lines.append("".join(line))
            layers.append("\n".join(lines))
        return "\n\n".join(layers)


def part1() -> int:
    points = load_points()
    return num_exposed_faces(points)


def part2() -> int:
    lava = LavaDroplet()
    return lava.exterior_surface()


if __name__ == "__main__":
    print("--- Part 1 ---")
    print("Number of exposed faces:", part1())
    print("--- Part 2 ---")
    print("Number of exterior faces:", part2())
