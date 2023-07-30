from aocd import get_data
from typing import Iterable

data = get_data(year=2022, day=1)


def packet_sums(data: str) -> Iterable[int]:
    return sorted(
        sum(int(x) for x in packet.split("\n")) for packet in data.split("\n\n")
    )


def part1() -> int:
    return packet_sums(data)[-1]


def part2() -> int:
    return sum(packet_sums(data)[-3:])


if __name__ == "__main__":
    print("--- Part 1 ---")
    print(part1())
    print("--- Part 2 ---")
    print(part2())
