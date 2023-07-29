import re
from copy import copy
from dataclasses import dataclass
from typing import Iterable, Self

from day12 import Distance

inf = Distance("inf")


class Valve:
    def __init__(
        self, name: str, flowrate: int, downstream_names: Iterable[str]
    ) -> None:
        self.name = name
        self.flowrate = flowrate
        self.downstream_names = downstream_names
        self.is_open = False

    def instanciate_downstream(self, valves: Iterable[Self]):
        self.downstream = dict()
        for v in self.downstream_names:
            self.downstream[v] = valves[v]

    def __repr__(self) -> str:
        return (
            f"Valve({self.name}, {self.flowrate}, [{', '.join(self.downstream_names)}])"
        )

    def __str__(self) -> str:
        return (
            f"Valve {self.name} has flow rate={self.flowrate}; "
            f"tunnels lead to valve{'s' if len(self.downstream_names) > 1 else ''} "
            f"{', '.join(self.downstream_names)}"
        )


@dataclass
class Move:
    target: str
    potential: int
    remaining_time: int

    def __repr__(self) -> str:
        return (
            f"Move(target={self.target.name}, "
            f"potential={self.potential}, "
            f"remaining_time={self.remaining_time})"
        )


class Graph:
    def __init__(self, path: str) -> None:
        self.valves = self.parse_file(path)
        self.max_total_flow = 0
        self.n_searched = 0
        self.non_zero_valves = sum(int(v.flowrate > 0) for v in self.valves.values())
        self.max_flow = sum(v.flowrate for v in self.valves.values())
        self.distances = GraphDistances(self)

    def parse_file(self, path: str) -> dict[str, Valve]:
        with open(path) as f:
            lines = f.read().splitlines()

        valves = dict()
        for line in lines:
            valve = self.parse_line(line)
            valves[valve.name] = valve

        for valve in valves.values():
            valve.instanciate_downstream(valves)

        return valves

    def parse_line(self, line: str) -> Valve:
        name = line.split(" ")[1]
        flowrate = int(re.findall(r"rate=(\d+)", line)[0])
        downstream_names = re.findall(r"(?:valve |valves )(.+)", line)[0].split(", ")
        return Valve(name, flowrate, downstream_names)

    def flow_potential(
        self, current_valve: Valve, remaining_time: int, open_valves: set[Valve]
    ):
        valve_potential = dict()
        for k, v in self.items():
            if v in open_valves or v.flowrate == 0:
                continue
            d = self.distances[current_valve.name, k]
            valve_potential[k] = max(0, remaining_time - d - 1) * v.flowrate
        return valve_potential

    def priority_search(
        self,
        current_valve: Valve = None,
        remaining_time: int = 30,
        open_valves: set[Valve] = None,
        total_flow: int = 0,
    ) -> int:
        if remaining_time == 0:
            self.n_searched += 1
            if total_flow > self.max_total_flow:
                self.max_total_flow = total_flow
            return total_flow
        if total_flow + remaining_time * self.max_flow <= self.max_total_flow:
            return 0
        if current_valve is None:
            current_valve = self.valves["AA"]
        if open_valves is None:
            open_valves = set()

        valve_potential = self.flow_potential(
            current_valve, remaining_time, open_valves
        )
        total_flow_potential = sum(valve_potential.values())
        current_flowrate = sum(v.flowrate for v in open_valves)

        if total_flow_potential == 0:
            return self.priority_search(
                current_valve,
                0,
                open_valves,
                total_flow + current_flowrate * remaining_time,
            )

        possible_moves = sorted(
            valve_potential.items(), key=lambda x: x[1], reverse=True
        )
        outcomes = set()
        for k, p in possible_moves:
            d = self.distances[current_valve.name, k]
            next_valve = self.valves[k]
            res = self.priority_search(
                next_valve,
                remaining_time - d - 1,
                open_valves | {next_valve},
                total_flow + current_flowrate * (d + 1),
            )
            outcomes.add(res)
        return max(outcomes)

    def flow_potential_multi_agent(
        self, current_valves: tuple[Valve], remaining_time: int, open_valves: set[Valve]
    ):
        v1, v2 = current_valves
        moves1 = self.flow_potential_single_agent(v1, remaining_time, open_valves)
        moves2 = self.flow_potential_single_agent(v2, remaining_time, open_valves)
        moves = []
        for m1 in moves1:
            for m2 in moves2:
                if m1.target == m2.target:
                    continue
                moves.append((m1, m2))
        return moves

    def flow_potential_single_agent(
        self, current_valve: Valve, remaining_time: int, open_valves: set[Valve]
    ):
        moves = []
        for target in self.valves.values():
            if target in open_valves or target.flowrate == 0:
                continue
            d = self.distances[current_valve.name, target.name]
            p = max(0, remaining_time - d - 1) * target.flowrate
            if p == 0:
                continue
            moves.append(Move(target, p, d + 1))
        if len(moves) == 0:
            moves = [Move(current_valve, 0, remaining_time)]
        return moves

    def multi_agent_search(
        self,
        current_valves: Valve = None,
        current_moves: tuple[Move, Move] = (None, None),
        remaining_time: int = 26,
        open_valves: set[Valve] = None,
        total_flow: int = 0,
    ) -> int:
        if remaining_time == 0:
            self.n_searched += 1
            if total_flow >= self.max_total_flow:
                self.max_total_flow = total_flow
            return total_flow
        if total_flow + remaining_time * self.max_flow <= self.max_total_flow:
            return 0
        if current_valves is None:
            current_valves = self.valves["AA"], self.valves["AA"]
        if open_valves is None:
            open_valves = set()

        v1, v2 = current_valves
        m1, m2 = current_moves
        current_flowrate = sum(v.flowrate for v in open_valves)

        if m1 is None and m2 is None:
            if v1 != v2:
                next_moves = self.flow_potential_multi_agent(
                    current_valves, remaining_time, open_valves
                )
            else:
                next_move_single = self.flow_potential_single_agent(
                    v1, remaining_time, open_valves
                )
                next_moves = []
                for i, m1 in enumerate(next_move_single[:-1]):
                    for m2 in next_move_single[i + 1 :]:
                        next_moves.append((m1, m2))
        elif m1 is None:
            next_move1 = self.flow_potential_single_agent(
                v1, remaining_time, open_valves | {m2.target}
            )
            next_moves = [(m, m2) for m in next_move1]
        elif m2 is None:
            next_move2 = self.flow_potential_single_agent(
                v2, remaining_time, open_valves | {m1.target}
            )
            next_moves = [(m1, m) for m in next_move2]
        else:
            raise Exception("This should not happen")

        total_flow_potential = sum(ma.potential + mb.potential for ma, mb in next_moves)
        if total_flow_potential == 0:
            return self.multi_agent_search(
                current_valves,
                (None, None),
                0,
                open_valves,
                total_flow + current_flowrate * remaining_time,
            )

        outcomes = set()
        move_priority = sorted(
            next_moves, key=lambda x: x[0].potential + x[1].potential, reverse=True
        )
        for m1, m2 in move_priority:
            time_to_next_move = min(m1.remaining_time, m2.remaining_time)
            next_open_valves = copy(open_valves)
            if m1.remaining_time - time_to_next_move == 0:
                next_v1 = m1.target
                next_m1 = None
                next_open_valves.add(m1.target)
            else:
                next_v1 = v1
                next_m1 = Move(
                    m1.target, m1.potential, m1.remaining_time - time_to_next_move
                )
            if m2.remaining_time - time_to_next_move == 0:
                next_v2 = m2.target
                next_m2 = None
                next_open_valves.add(m2.target)
            else:
                next_v2 = v2
                next_m2 = Move(
                    m2.target, m2.potential, m2.remaining_time - time_to_next_move
                )
            res = self.multi_agent_search(
                (next_v1, next_v2),
                (next_m1, next_m2),
                remaining_time - time_to_next_move,
                next_open_valves,
                total_flow + current_flowrate * time_to_next_move,
            )
            outcomes.add(res)
        return max(outcomes)

    def items(self) -> Iterable[tuple[str, Valve]]:
        return self.valves.items()

    def values(self) -> Iterable[Valve]:
        return self.valves.values()

    def __getitem__(self, key: str) -> Valve:
        return self.valves[key]

    def __len__(self) -> int:
        return len(self.valves)


@dataclass
class Node:
    valve: Valve
    d: Distance
    visited: bool = False
    prev: "Node" = None


class GraphDistances:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.distances: dict[str, dict[str, Distance]] = {
            k: self.calculate_distances(v) for k, v in graph.items()
        }

    def next_unvisited(self, unvisited) -> Node:
        min_index = 0
        min_distance = inf
        for i, node in enumerate(unvisited):
            if node.d < min_distance:
                min_index = i
                min_distance = node.d
        return unvisited.pop(min_index)

    def calculate_distances(self, start_node: Valve) -> dict[str, int]:
        nodes = {k: Node(v, inf) for k, v in self.graph.items()}
        nodes[start_node.name].d = Distance(0)
        unvisited = [n for n in nodes.values()]
        while len(unvisited) > 0:
            current_node = self.next_unvisited(unvisited)
            new_distance = current_node.d + 1
            for downstream_name in current_node.valve.downstream:
                downstream_node = nodes[downstream_name]
                if downstream_node.visited:
                    continue
                if new_distance < downstream_node.d:
                    downstream_node.d = new_distance
                    downstream_node.prev = current_node
            current_node.visited = True
        return {k: int(n.d) for k, n in nodes.items()}

    def __getitem__(self, key: tuple[str, str]) -> int:
        k1, k2 = key
        return self.distances[k1][k2]

    def __str__(self) -> str:
        lines = []
        for k1, d1 in self.distances.items():
            for k2, d2 in d1.items():
                lines.append(f"Distance fromm {k1} to {k2}: {d2:>3}")
        return "\n".join(lines)


# g = Graph('day16-input')
# g = Graph('input.txt')
# print(g.priority_search())
# g.multi_agent_search()
