from aocd.models import Puzzle  # type: ignore

puzzle = Puzzle(year=2022, day=25)


class SNAFU:
    value_map: dict[str, int] = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
    rvalue_map: dict[int, str] = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}

    def __init__(self, x: int | str) -> None:
        if isinstance(x, int):
            self.value = self.from_int(x)
        elif isinstance(x, str):
            self.value = x
        else:
            raise NotImplementedError

    def from_int(self, n: int) -> str:
        rmap = {(k + 2) % 5: v for k, v in self.rvalue_map.items()}
        n, r = divmod(n + 2, 5)
        value = [rmap[r]]
        while n > 0:
            n, r = divmod(n + 2, 5)
            value.append(rmap[r])
        return "".join(reversed(value))

    def __int__(self) -> int:
        n = 0
        for i, d in enumerate(reversed(self.value)):
            n += self.value_map[d] * 5**i
        return n

    def __repr__(self) -> str:
        return self.value


def part1(data: str) -> str:
    total = sum([int(SNAFU(s)) for s in data.splitlines()])
    return str(SNAFU(total))


if __name__ == "__main__":
    print(part1(puzzle.input_data))
