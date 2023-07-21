
class SandSimulator:
    def __init__(self, path, floor=False) -> None:
        self.cave = dict()
        self.populate_cave(path)
        self.calculate_bounds()
        if floor:
            self.floor = self.ymax + 2
            self.ymax = self.floor
        self.sand_source = (500, 0)

    @staticmethod
    def split_coords(coords):
        return [int(c) for c in coords.split(',')]

    def populate_cave(self, path):
        with open(path) as f:
            lines = f.read().splitlines()

        for line in lines:
            segments = line.split(' -> ')
            for start, end in zip(segments[:-1], segments[1:]):
                print(start, end)
                x1, y1 = self.split_coords(start)
                x2, y2 = self.split_coords(end)
                if x1 == x2:
                    x = x1
                    start_y, end_y = min([y1,y2]), max([y1,y2])
                    for y in range(start_y, end_y+1):
                        self.cave[(x, y)] = '#'
                elif y1 == y2:
                    y = y1
                    start_x, end_x = min([x1,x2]), max([x1,x2])
                    for x in range(start_x, end_x+1):
                        self.cave[(x, y)] = '#'
                else:
                    raise ValueError('Invalid input file.')
    
    def calculate_bounds(self):
        x_values = [r[0] for r in self.cave.keys()]
        y_values = [r[1] for r in self.cave.keys()]
        self.xmin = min(x_values)
        self.xmax = max(x_values)
        self.ymin = min(y_values)
        self.ymax = max(y_values)
    
    def cave_lookup(self, x, y):
        return self.cave.get((x, y), '.')
    
    def is_blocked(self, x, y):
        if self.floor and y == self.floor:
            return True
        return (x,y) in self.cave
    
    def in_bounds(self, x, y):
        return self.xmin <= x <= self.xmax and y < self.ymax

    def add_grain_no_floor(self):
        x, y = self.sand_source
        y = max(y, self.ymin-1)
        stopped = False
        while not stopped and self.in_bounds(x, y):
            if not self.is_blocked(x, y+1):
                y += 1
            elif not self.is_blocked(x-1, y+1):
                x -= 1
                y += 1
            elif not self.is_blocked(x+1, y+1):
                x += 1
                y += 1
            else:
                stopped = True
        if stopped:
            self.cave[(x,y)] = 'o'
            self.ymin = min(self.ymin, y)
        return stopped

    def add_grain_floor(self):
        x, y = self.sand_source
        y = max(y, self.ymin-1)
        stopped = False
        while not stopped and not self.is_blocked(x, y):
            print(x, y)
            while not self.is_blocked(x, y+1):
                y += 1
            if not self.is_blocked(x-1, y+1):
                x -= 1
                y += 1
            elif not self.is_blocked(x+1, y+1):
                x += 1
                y += 1
            else:
                stopped = True
        if stopped:
            self.cave[(x,y)] = 'o'
            self.ymin = min(self.ymin, y)
            self.xmin = min(self.xmin, x)
            self.xmax = max(self.xmax, x)
        return stopped
    
    def add_grain(self):
        if self.floor is None:
            return self.add_grain_no_floor()
        else:
            return self.add_grain_floor()

    def __str__(self) -> str:
        lines = []
        for y in range(self.ymin, self.ymax+1):
            if self.floor is not None and y == self.floor:
                lines.append(f'{y:>3} ' + '#' * (self.xmax + 1 - self.xmin) + '\n')
                break
            line = [f'{y:>3} ']
            for x in range(self.xmin, self.xmax + 1):
                line.append(self.cave_lookup(x, y))
            lines.append(''.join(line) + '\n')
        return ''.join(lines)
    
# sim = SandSimulator('tmp', floor=True)
sim = SandSimulator('day14-input', floor=True)
total_grains = 0
while sim.add_grain():
    total_grains += 1
    print(total_grains)
print(sim)
print(total_grains)