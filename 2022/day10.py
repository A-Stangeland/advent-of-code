from typing import Iterable

class CPU:
    def __init__(self, recording_cycles: list[int]) -> None:
        self.X = 1
        self.cycle_counter = 0
        self.recording_cycles = recording_cycles
        self.signal_strengths: list[int] = []
        self.last_instruction = None
        self.crt = CRT(self)
    
    def addx(self, V: int) -> None:
        self.cycle()
        self.cycle()
        self.X += V

    def noop(self) -> None:
        self.cycle()

    def cycle(self) -> None:
        self.crt.update()
        self.cycle_counter += 1
        if self.cycle_counter in self.recording_cycles:
            print(self)
            self.signal_strengths.append(self.X * self.cycle_counter)

    def parse_instruction(self, instruction: str):
        command_args = instruction.split(' ')
        command = command_args[0]
        self.last_instruction = instruction
        if command == 'noop':
            self.noop()
        elif command == 'addx':
            V = int(command_args[1])
            self.addx(V)
    
    def parse_input(self, path: str):
        with open(path) as f:
            lines = f.read().splitlines()
        for line in lines:
            self.parse_instruction(line)

    def __str__(self) -> str:
        lines = [
            f"Clock cycle: {self.cycle_counter}\n",
            f"Value of X: {self.X}\n",
            f"Last instruction: {self.last_instruction}\n",
            f"Recording cycles: {self.recording_cycles}\n"
            f"Signal strengths: {self.signal_strengths}\n"
            f"Sum of signal strengths: {sum(self.signal_strengths)}\n"
            f"Screen:\n",
            f"{str(self.crt)}"
        ]
        return ''.join(lines)

class CRT:
    def __init__(self, cpu: CPU) -> None:
        self.cpu = cpu
        self.screen = [['.' for _ in range(40)] for _ in range(6)]
        self.w = 40
        self.h = 6
    
    def draw_pixel(self, x: int, y: int):
        if abs(x - self.cpu.X) <= 1:
            self.screen[y][x] = '#'
        else:
            self.screen[y][x] = '.'

    def update(self):
        x = self.cpu.cycle_counter % self.w
        y = (self.cpu.cycle_counter // 40) % self.h
        self.draw_pixel(x, y)
    
    def __str__(self) -> str:
        lines = [''.join(line) + '\n' for line in self.screen]
        return ''.join(lines)

cpu = CPU([20, 60, 100, 140, 180, 220])
cpu.parse_input('day10-input')
print(cpu)