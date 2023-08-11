from aocd.models import Puzzle  # type: ignore

from typing import Self, Optional, Iterable

puzzle = Puzzle(year=2022, day=20)


class CiferElement:
    def __init__(self, value: int):
        self.value = value
        self.prev: Optional[Self] = None
        self.next: Optional[Self] = None

    def __repr__(self) -> str:
        prev_value = self.prev.value if self.prev is not None else "None"
        next_value = self.next.value if self.next is not None else "None"
        return f"CiferElement(n={self.value}, prev={prev_value}, next={next_value})"


def link(e1: CiferElement, e2: CiferElement):
    e1.next = e2
    e2.prev = e1


class Decrypter:
    def __init__(self, data: str) -> None:
        self.parse_data(data)

    def parse_data(self, data: str) -> None:
        self.queue: list[CiferElement] = []
        lines = data.splitlines()
        for n in lines:
            e = CiferElement(int(n))
            if e.value == 0:
                self.zero = e
            if len(self.queue) > 0:
                link(self.queue[-1], e)
            self.queue.append(e)
        link(self.queue[-1], self.queue[0])
        self.cifer_lenght = len(self.queue)

    def shift_element(self, e: CiferElement):
        old_prev = e.prev
        old_next = e.next
        link(old_prev, old_next)
        new_prev = old_prev
        if e.value > 0:
            shift = e.value % (self.cifer_lenght - 1)
            for _ in range(shift):
                new_prev = new_prev.next
        if e.value < 0:
            shift = -e.value % (self.cifer_lenght - 1)
            for _ in range(shift):
                new_prev = new_prev.prev
        new_next = new_prev.next
        link(new_prev, e)
        link(e, new_next)

    def nth_after_zero(self, n: int) -> int:
        shift = n % self.cifer_lenght
        pointer = self.zero
        for _ in range(shift):
            pointer = pointer.next
        print(pointer.value)
        return pointer.value

    def __len__(self) -> int:
        return self.cifer_lenght

    def elements(self) -> Iterable[CiferElement]:
        current = self.zero
        for _ in range(self.cifer_lenght):
            yield current
            current = current.next

    def values(self) -> Iterable[int]:
        current = self.zero
        for _ in range(self.cifer_lenght):
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return ", ".join(str(n) for n in self.values())

    def process_queue(self):
        while self.queue:
            e = self.queue.pop(0)
            self.shift_element(e)


def part1(data: str) -> str:
    d = Decrypter(data)
    print(d)
    d.process_queue()
    return str(sum(d.nth_after_zero(n) for n in [1000, 2000, 3000]))


def part2(data: str) -> str:
    pass


if __name__ == "__main__":
    print("--- Part 1 ---")
    # with open("input.txt") as f:
    # print("Sum of positions:", part1(f.read()))
    # print("Sum of positions:", part1(puzzle.examples[0].input_data))
    print("Sum of positions:", part1(puzzle.input_data))
    # print("--- Part 2 ---")
    # print("Product of first three blueprints:", part2(puzzle.input_data))
