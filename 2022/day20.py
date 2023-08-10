from aocd.models import Puzzle  # type: ignore
from dataclasses import dataclass

puzzle = Puzzle(year=2022, day=20)


@dataclass
class CiferElement:
    position: int
    value: int


class Decrypter:
    def __init__(self, data: str) -> None:
        self.parse_data(data)

    def parse_data(self, data: str) -> None:
        self.initial_queue = []
        self.shifted_positions = []
        for i, n in enumerate(data.splitlines()):
            e = CiferElement(i, int(n))
            self.initial_queue.append(e)
            self.shifted_positions.append(e)
            if e.value == 0:
                self.zero = e
        self.cifer_lenght = len(self.initial_queue)

    def print_move(self, e: CiferElement, new_position: int):
        left = self.shifted_positions[new_position].value
        right = self.shifted_positions[(new_position + 1) % self.cifer_lenght].value
        print(f"{e.value} moves between {left} and {right}")

    def get_new_position(self, e: CiferElement):
        if e.value >= 0:
            return (e.position + e.value) % self.cifer_lenght
        else:
            return (e.position + e.value) % self.cifer_lenght

    def shift_element(self, e: CiferElement):
        current_position = e.position
        new_position = self.get_new_position(e)
        self.print_move(e, new_position)
        if new_position > current_position:
            for other_e in self.shifted_positions[
                current_position + 1 : new_position + 1
            ]:
                other_e.position -= 1
            self.shifted_positions.pop(current_position)
            self.shifted_positions.insert(new_position, e)
            e.position = new_position
        elif new_position < current_position:
            # new_position += 1
            for other_e in self.shifted_positions[new_position:current_position]:
                other_e.position += 1
            self.shifted_positions.pop(current_position)
            self.shifted_positions.insert(new_position, e)
            e.position = new_position

    def nth_after_zero(self, n: int) -> int:
        i = (self.zero.position + n) % self.cifer_lenght
        e = self.shifted_positions[i]
        print(e.value)
        return e.value

    def __str__(self) -> str:
        return (
            ", ".join(str(e.value) for e in self.shifted_positions)
            + "\n"
            + ", ".join(str(e.position) for e in self.shifted_positions)
        )

    def process_queue(self):
        print("Initial arangement:")
        # print(self)
        while self.initial_queue:
            # print()
            e = self.initial_queue.pop(0)
            self.shift_element(e)
            # print(self)

    def validate_index(self):
        for i, e in enumerate(self.shifted_positions):
            print(i, e.position)
            if i != e.position:
                raise IndexError()


def part1(data: str) -> str:
    d = Decrypter(data)
    d.process_queue()
    d.validate_index()
    return sum(d.nth_after_zero(n) for n in [1000, 2000, 3000])


def part2(data: str) -> str:
    pass


if __name__ == "__main__":
    print("--- Part 1 ---")
    print("Sum of positions:", part1(puzzle.examples[0].input_data))
    # print("Sum of positions:", part1(puzzle.input_data))
    # print("--- Part 2 ---")
    # print("Product of first three blueprints:", part2(puzzle.input_data))
# d = Decrypter(puzzle.examples[0].input_data)
# d.process_queue()
