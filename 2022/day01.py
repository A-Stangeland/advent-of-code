from aocd.models import Puzzle
from typing import Iterable

puzzle = Puzzle(year=2022, day=1)
# data = get_data(year=2022, day=1)


def packet_sums(data: str) -> Iterable[int]:
    return sorted(
        sum(int(x) for x in packet.split("\n")) for packet in data.split("\n\n")
    )


def part1(data: str) -> str:
    max_sum = packet_sums(data)[-1]
    return str(max_sum)


def part2(data: str) -> str:
    top_three_sum = sum(packet_sums(data)[-3:])
    return str(top_three_sum)


if __name__ == "__main__":
    print("--- Part 1 ---")
    print(part1(puzzle.input_data))
    print("--- Part 2 ---")
    print(part2(puzzle.input_data))
    print(puzzle.examples)
