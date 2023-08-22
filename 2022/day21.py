from aocd.models import Puzzle  # type: ignore

puzzle = Puzzle(year=2022, day=21)


class MonkeyTroop:
    def __init__(self, data: str) -> None:
        self.parse_data(data)

    def parse_data(self, data: str):
        self.known_numbers: dict[str, int] = dict()
        self.unknown_numbers: dict[str, tuple[str, str, str]] = dict()
        for line in data.splitlines():
            name, yell = line.split(": ")
            if yell.isnumeric():
                self.known_numbers[name] = int(yell)
                continue
            m1, op, m2 = yell.split(" ")
            self.unknown_numbers[name] = (m1, op, m2)

    def calculate_number(self, name: str):
        if name in self.known_numbers:
            return self.known_numbers[name]
        m1, op, m2 = self.unknown_numbers.pop(name)
        n1 = self.calculate_number(m1)
        print(m1, n1)
        n2 = self.calculate_number(m2)
        print(m2, n2)
        match op:
            case "+":
                return n1 + n2
            case "-":
                return n1 - n2
            case "*":
                return n1 * n2
            case "/":
                return n1 // n2
            case _:
                raise ValueError(f"{op} is not a valid operation.")

    def get_formula(self, name: str):
        if name == "humn":
            return "x"
        if name in self.known_numbers:
            return self.known_numbers[name]
        m1, op, m2 = self.unknown_numbers.pop(name)
        n1 = self.get_formula(m1)
        n2 = self.get_formula(m2)
        if name == "root":
            return (n1, "=", n2)
        if isinstance(n1, (str, tuple)) or isinstance(n2, (str, tuple)):
            return (n1, op, n2)
        match op:
            case "+":
                return n1 + n2
            case "-":
                return n1 - n2
            case "*":
                return n1 * n2
            case "/":
                return n1 // n2
            case _:
                raise ValueError(f"{op} is not a valid operation.")


def invert_formula(formula: tuple):
    left, _, right = formula
    while left != "x":
        v1, op, v2 = left
        match op:
            case "+":
                if isinstance(v1, int):
                    left = v2
                    right = right - v1
                elif isinstance(v2, int):
                    left = v1
                    right = right - v2
            case "-":
                if isinstance(v1, int):
                    left = v2
                    right = v1 - right
                elif isinstance(v2, int):
                    left = v1
                    right = right + v2
            case "*":
                if isinstance(v1, int):
                    left = v2
                    right = right // v1
                elif isinstance(v2, int):
                    left = v1
                    right = right // v2
            case "/":
                if isinstance(v1, int):
                    left = v2
                    right = v1 // right
                elif isinstance(v2, int):
                    left = v1
                    right = right * v2
            case _:
                raise ValueError()
    return right


def part1(data: str):
    troop = MonkeyTroop(data)
    return troop.calculate_number("root")


def part2(data: str):
    troop = MonkeyTroop(data)
    formula = troop.get_formula("root")
    print(formula)
    return invert_formula(formula)


if __name__ == "__main__":
    # print("--- Part 1 ---")
    # print("root number:", part1(puzzle.input_data))
    print("--- Part 2 ---")
    print("humn number:", part2(puzzle.input_data))
