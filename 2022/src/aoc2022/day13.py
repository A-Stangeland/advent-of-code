from typing import Self
from functools import total_ordering


@total_ordering
class Packet:
    def __init__(self, s: str) -> None:
        self.value = self.parse(s)

    def parse(self, s: str) -> list:
        self.i = 0
        self.buffer = [c for c in s]
        packet = self.__recur()
        return packet

    def __recur(self) -> list:
        result = None
        int_buffer = []
        while self.buffer:
            c = self.buffer.pop(0)
            if c == "[":
                if result is None:
                    result = []
                else:
                    self.buffer.insert(0, c)
                    result.append(self.__recur())
            elif c == "]":
                if int_buffer:
                    result.append(int("".join(int_buffer)))
                return result
            elif c == ",":
                if int_buffer:
                    result.append(int("".join(int_buffer)))
                    int_buffer = []
                else:
                    pass
            elif c.isdigit():
                int_buffer.append(c)
            else:
                raise ValueError(f"Encountered unexpected value while parsing: {c}")

    def compare_packets(self, left: list, right: list, level=0) -> bool:
        for L, R in zip(left, right):
            if isinstance(L, int) and isinstance(R, int):
                if L > R:
                    return False
                if L < R:
                    return True
            elif isinstance(L, list) and isinstance(R, list):
                result = self.compare_packets(L, R, level + 1)
                if result is not None:
                    return result
            else:
                if isinstance(L, int):
                    result = self.compare_packets([L], R, level + 1)
                    if result is not None:
                        return result
                else:
                    result = self.compare_packets(L, [R], level + 1)
                    if result is not None:
                        return result
        if len(left) > len(right):
            return False
        if len(left) < len(right):
            return True
        return None

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other: Self) -> bool:
        return self.compare_packets(self.value, other.value)

    def __eq__(self, other: Self) -> bool:
        return self.value == other.value


def parse_packet_pairs(path: str) -> list[tuple[Packet, Packet]]:
    with open(path) as f:
        lines = f.read().splitlines()
    packets = []
    while lines:
        packet1 = Packet(lines.pop(0))
        packet2 = Packet(lines.pop(0))
        if lines:
            print(len(lines.pop(0)))
        packets.append((packet1, packet2))
    return packets


def parse_packets(path: str) -> list[Packet]:
    with open(path) as f:
        lines = f.read().splitlines()
    packets = []
    for line in lines:
        if len(line) > 0:
            packets.append(Packet(line))
    d1 = Packet("[[2]]")
    d2 = Packet("[[6]]")
    packets.append(d1)
    packets.append(d2)
    return packets, d1, d2


def calculate_index_sum(path):
    packets = parse_packet_pairs(path)
    total = 0
    for i, (p1, p2) in enumerate(packets):
        print(f"== Pair {i+1} ==")
        print(f"{p1} vs {p2}")
        if p1 < p2:
            print("Is ordered")
            total += i + 1
        else:
            print("Is not ordered")
        print()
    print(f"Sum of indices of ordered pairs: {total}")


def sort_packets():
    pass


packets, d1, d2 = parse_packets("day13-input")
packets = sorted(packets)
i1 = packets.index(d1) + 1
i2 = packets.index(d2) + 1
print(i1 * i2)
