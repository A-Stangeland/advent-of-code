from typing import Iterable, Self, Optional
import re

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
    
    def __getitem__(self, key: str) -> Valve:
        return self.valves[key]

class GraphTraverser:
    def __init__(self, g: Graph) -> None:
        self.g = g
        self.current_valve = g['AA']
        self.remaining_time = 30
    
    def goto(self, name: str) -> None:
        self.current_valve = self.current_valve.downstream[name]
        self.remaining_time -= 1
    
    def open_valve(self):
        if self.current_valve.is_open:
            raise ValueError(f"Valve {self.current_valve.name} is already open.")
        self.current_valve.is_open = True
        self.remaining_time -= 1

g = Graph('day16-input')
t = GraphTraverser(g)
print(t.current_valve)