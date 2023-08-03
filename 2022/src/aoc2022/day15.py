import re
from typing import Self, Iterable


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def coords(self):
        return self.x, self.y

    def __eq__(self, other: Self) -> bool:
        return self.coords == other.coords

    def __hash__(self) -> int:
        return hash(self.coords)

    def dist(self, other: Self | tuple[int, int]) -> int:
        if isinstance(other, tuple):
            x, y = other
            return abs(self.x - x) + abs(self.y - y)
        else:
            return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self) -> str:
        return str(self.coords)


class SensorReport:
    x_pattern = r"x=(-?\d+)"
    y_pattern = r"y=(-?\d+)"

    def __init__(self, report: str) -> None:
        sensor_coords, beacon_coords = self.parse_report(report)
        self.sensor = Point(*sensor_coords)
        self.beacon = Point(*beacon_coords)
        self.dist = dist(self.sensor, self.beacon)

    def parse_report(self, report: str):
        x_matches = re.findall(self.x_pattern, report)
        y_matches = re.findall(self.y_pattern, report)
        sensor_x = int(x_matches[0])
        sensor_y = int(y_matches[0])
        beacon_x = int(x_matches[1])
        beacon_y = int(y_matches[1])
        return (sensor_x, sensor_y), (beacon_x, beacon_y)

    def adjusted_dist(self, y_line: int) -> int:
        return self.dist - abs(self.sensor.y - y_line)

    def __str__(self) -> str:
        return f"""SensorReport
- Sensor: {self.sensor}
- Beacon: {self.beacon}
- Distance: {self.dist}"""


def dist(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def load_reports(path: str) -> list[SensorReport]:
    with open(path) as f:
        lines = f.read().splitlines()
    reports = [SensorReport(line) for line in lines]
    return reports


def num_impossible_positions(reports: Iterable[SensorReport], y_line: int) -> int:
    beacons = set([r.beacon for r in reports])
    beacons_on_yline = list(filter(lambda b: b.y == y_line, beacons))
    total = -len(beacons_on_yline)
    reports = filter(lambda r: r.adjusted_dist(y_line) > 0, reports)
    reports = sorted(reports, key=lambda r: r.sensor.x)
    r = reports[0]
    total += 2 * r.adjusted_dist(y_line) + 1
    prev_max = r.sensor.x + r.adjusted_dist(y_line)
    print(r)
    print(r.adjusted_dist(y_line))
    print(r.sensor.x - r.adjusted_dist(y_line), r.sensor.x + r.adjusted_dist(y_line))
    for r in reports[1:]:
        start = max(r.sensor.x - r.adjusted_dist(y_line), prev_max + 1)
        end = r.sensor.x + r.adjusted_dist(y_line)
        print(r)
        print(start, end, max(0, end - start + 1))
        # print(end - start + 1)
        total += max(0, end - start + 1)
        prev_max = max(prev_max, end)
    print(total)


def print_search_space(reports: Iterable[SensorReport], bounds: tuple[int, int]):
    l, u = bounds
    lines = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for y in range(l, u + 1):
        line = [f"{y:>2} "]
        for x in range(l, u + 1):
            c = "."
            for i, r in enumerate(reports):
                if r.sensor.coords == (x, y):
                    c = bcolors.OKBLUE + "S" + bcolors.ENDC
                    break
                elif r.beacon.coords == (x, y):
                    c = bcolors.OKGREEN + "B" + bcolors.ENDC
                    break
                elif r.sensor.dist((x, y)) <= r.dist:
                    c = alphabet[i]
                    break
            line.append(c)
        lines.append("".join(line) + "\n")
    print("".join(lines))


def get_translate_dist(p: Point, r: SensorReport) -> int:
    x, y = p.coords
    t = (y + r.sensor.x - x - r.sensor.y + r.dist) // 2 + 1
    return t


def print_t_dist(r: SensorReport):
    sx, sy = r.sensor.coords
    lines = []
    for y in range(sy - r.dist, sy + r.dist + 1):
        line = [f"{y:>2} "]
        for x in range(sx - r.dist, sx + r.dist + 1):
            p = Point(x, y)
            c = "."
            if (x, y) == r.sensor.coords:
                c = "S"
            elif dist(p, r.sensor) <= r.dist:
                c = str(get_translate_dist(p, r))
            line.append(c)
        lines.append("".join(line) + "\n")
    print("".join(lines))


def find_beacon(reports: Iterable[SensorReport], bounds: tuple[int, int]) -> int:
    l, u = bounds
    for row in reversed(range(l, 2 * u + 1)):
        if row <= u:
            y = row
            x = 0
        else:
            y = u
            x = row - u
        while y >= 0 and x <= u:
            p = Point(x, y)
            print(p)
            is_open = True
            for r in reports:
                if dist(p, r.sensor) <= r.dist:
                    t = get_translate_dist(p, r)
                    y -= t
                    x += t
                    is_open = False
                    break
            if is_open:
                print(p, 4_000_000 * x + y)
                return p


reports = load_reports("day15-input")
searched = find_beacon(reports, (0, 4_000_000))
