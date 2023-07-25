import re
from dataclasses import dataclass
from typing import Iterable, Optional, Self

from day12 import Distance

inf = Distance('inf')

class Valve:
    def __init__(self, name: str, flowrate: int, downstream_names: Iterable[str]) -> None:
        self.name = name
        self.flowrate = flowrate
        self.downstream_names = downstream_names
        self.is_open = False
    
    def instanciate_downstream(self, valves: Iterable[Self]):
        self.downstream = dict()
        for v in self.downstream_names:
            self.downstream[v] = valves[v]
    
    def __str__(self) -> str:
        return f"Valve {self.name} has flow rate={self.flowrate}; tunnels lead to valve{'s' if len(self.downstream_names) > 1 else ''} {', '.join(self.downstream_names)}"


class Graph:
    def __init__(self, path: str) -> None:
        self.valves = self.parse_file(path)
        self.max_flow = 0
        self.n_searched = 0
        self.non_zero_valves = sum([int(v.flowrate > 0) for v in self.valves.values()])
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
        name = line.split(' ')[1]
        flowrate = int(re.findall(r'rate=(\d+)', line)[0])
        downstream_names = re.findall(r'(?:valve |valves )(.+)', line)[0].split(', ')
        return Valve(name, flowrate, downstream_names)

    def flow_potential(self, current_valve: Valve, remaining_time: int, open_valves: set[Valve]):
        valve_potential = dict()
        for k, v in self.items():
            if v in open_valves or v.flowrate == 0:
                continue
            d = self.distances[current_valve.name, k]
            valve_potential[k] = max(0, remaining_time - d - 1) * v.flowrate
        return valve_potential
    
    def priority_search(self, current_valve: Valve=None, remaining_time: int=30, open_valves: set[Valve]=None, total_flow: int=0, moves=())  -> int:
        if remaining_time == 0:
            self.n_searched += 1
            if total_flow > self.max_flow:
                for m in moves:
                    print(m)
                print('>>> Total flow:', total_flow)
                print('>>> N searched:', self.n_searched)
                print()
                self.max_flow = total_flow
            return total_flow
        if current_valve is None:
            current_valve = self.valves['AA']
        if open_valves is None:
            open_valves = set()
        
        valve_potential = self.flow_potential(current_valve, remaining_time, open_valves)
        total_flow_potential = sum(valve_potential.values())
        current_flowrate = sum([v.flowrate for v in open_valves])

        if total_flow_potential == 0:
            return self.priority_search(
                current_valve, 
                0, 
                open_valves, 
                total_flow + current_flowrate*remaining_time, 
                moves + (f'{30-remaining_time:>2} Wait {remaining_time} minutes, flow rate: {current_flowrate:>4}, total flow: {total_flow:>4}',)
            )
        
        possible_moves = sorted(valve_potential.items(), key=lambda x: x[1], reverse=True)
        outcomes = set()
        for k, p in possible_moves:
            d = self.distances[current_valve.name, k]
            next_valve = self.valves[k]
            res = self.priority_search(
                next_valve, 
                remaining_time-d-1, 
                open_valves | {next_valve}, 
                total_flow + current_flowrate*(d+1), 
                moves + (f'{30-remaining_time:>2} Move to and open {next_valve.name}, flow rate: {current_flowrate:>4}, total flow: {total_flow:>4}',)
            )
            outcomes.add(res)
        return max(outcomes)

    def items(self) -> Iterable[tuple[str, Valve]]:
        return self.valves.items()

    def __getitem__(self, key: str) -> Valve:
        return self.valves[key]

    def __len__(self) -> int:
        return len(self.valves)

@dataclass
class Node:
    valve: Valve
    d: Distance
    visited: bool=False
    prev: "Node"=None

    
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
    
    def __getitem__(self, key: tuple[str,str]) -> int:
        k1, k2 = key
        return self.distances[k1][k2]

    def __str__(self) -> str:
        lines = []
        for k1, d1 in self.distances.items():
            for k2, d2 in d1.items():
                lines.append(f'Distance fromm {k1} to {k2}: {d2:>3}')
        return '\n'.join(lines)

g = Graph('day16-input')
g.priority_search()