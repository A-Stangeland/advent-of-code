from typing import Self, Callable

class Knot:
    def __init__(self, ahead: Self, behind=None) -> None:
        self.ahead = ahead
        self.behind = behind
        self.x: int = 0
        self.y: int = 0

    def update_position(self):
        if self.ahead.x - self.x > 1:
            self.x += 1
            if self.ahead.y > self.y:
                self.y += 1
            elif self.ahead.y < self.y:
                self.y -= 1
        elif self.ahead.x - self.x < -1:
            self.x -= 1
            if self.ahead.y > self.y:
                self.y += 1
            elif self.ahead.y < self.y:
                self.y -= 1
                
        if self.ahead.y - self.y > 1:
            self.y += 1
            if self.ahead.x > self.x:
                self.x += 1
            elif self.ahead.x < self.x:
                self.x -= 1
        elif self.ahead.y - self.y < -1:
            self.y -= 1
            if self.ahead.x > self.x:
                self.x += 1
            elif self.ahead.x < self.x:
                self.x -= 1
        
        if self.behind is not None:
            self.behind.update_position()
    
    def add_behind(self):
        self.behind = Knot(self)
        return self.behind

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

class Head(Knot):
    def __init__(self) -> None:
        super().__init__(ahead=None)
    
    def U(self) -> None:
        self.y += 1
        self.behind.update_position()
    
    def D(self) -> None:
        self.y -= 1
        self.behind.update_position()
    
    def L(self) -> None:
        self.x -= 1
        self.behind.update_position()
    
    def R(self) -> None:
        self.x += 1
        self.behind.update_position()

class Rope:
    def __init__(self, length: int=2) -> None:
        self.lenght = length
        self.populate(length)
        self.tail_history = [self.tail.position]
    
    def populate(self, length: int) -> None:
        self.head = Head()
        current_knot = self.head
        for _ in range(length - 1):
            current_knot = current_knot.add_behind()
        self.tail = current_knot

    def record_tail(self) -> None:
        self.tail_history.append(self.tail.position)

    def multistep(move: Callable[[Self], None]) -> Callable[[Self, int], None]:
        def move_n_times(self, n):
            for _ in range(n):
                move(self)
                self.record_tail()
        return move_n_times

    @multistep
    def U(self):
        self.head.U()

    @multistep
    def D(self):
        self.head.D()

    @multistep
    def L(self):
        self.head.L()

    @multistep
    def R(self):
        self.head.R()

    @property
    def unique_tail_positions(self):
        return len(set(self.tail_history))
    
    def __str__(self) -> str:
        xmin = min([p[0] for p in self.tail_history])
        xmax = max([p[0] for p in self.tail_history])
        ymin = min([p[1] for p in self.tail_history])
        ymax = max([p[1] for p in self.tail_history])
        xmin = min(xmin, self.head.x)
        xmax = max(xmax, self.head.x)
        ymin = min(ymin, self.head.y)
        ymax = max(ymax, self.head.y)
        lines = []
        for y in range(ymin, ymax+1):
            line = []
            for x in range(xmin, xmax+1):
                c = '.'
                if (x, y) in self.tail_history:
                    c = '#'
                if (x, y) == (0, 0):
                    c = 'S'
                if (x, y) == self.tail.position:
                    c = 'T'
                if (x, y) == self.head.position:
                    c = 'H'
                line.append(c)
            lines.append(''.join(line) + '\n')
        return ''.join(lines[::-1])

class RopeSimulator:
    def __init__(self, path: str, rope_length: int) -> None:
        self.moves = self.move_generator(path)
        self.rope = Rope(rope_length)

    @staticmethod
    def move_generator(path):
        with open(path) as f:
            moves = f.read().splitlines()
    
        for move in moves:
            direction, steps = move.split(' ')
            yield direction, int(steps)

    def simulate(self):
        for direction, n in self.moves:
            match direction:
                case 'U': self.rope.U(n)
                case 'D': self.rope.D(n)
                case 'L': self.rope.L(n)
                case 'R': self.rope.R(n)
        print(f'Number of unique tail positions: {self.rope.unique_tail_positions}')
        print(self.rope)

r = RopeSimulator('day09-input', 10)
r.simulate()