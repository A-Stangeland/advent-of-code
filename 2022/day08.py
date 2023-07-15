import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GridIterator:
    def __init__(self, grid: np.ndarray, i: int, j: int) -> None:
        self.grid = grid
        self.n = grid.shape[0]
        self.m = grid.shape[1]
        self.i = i
        self.j = j
        self.u = 0
        self.d = 0
        self.l = 0
        self.r = 0

    def calculate_scenic_score(self):
        self.up()
        self.down()
        self.left()
        self.right()
        return self.scenic_score

    def up(self):
        i, j = self.i, self.j
        while True:
            i -= 1
            if not self.valid_index(i, j):
                break
            self.u += 1
            if self.is_taller(i, j):
                break

    def down(self):
        i, j = self.i, self.j
        while True:
            i += 1
            if not self.valid_index(i, j):
                break
            self.d += 1
            if self.is_taller(i, j):
                break

    def left(self):
        i, j = self.i, self.j
        while True:
            j -= 1
            if not self.valid_index(i, j):
                break
            self.l += 1
            if self.is_taller(i, j):
                break
            
    def right(self):
        i, j = self.i, self.j
        while True:
            j += 1
            if not self.valid_index(i, j):
                break
            self.r += 1
            if self.is_taller(i, j):
                break
            
    def valid_index(self, i, j):
        if 0 <= i < self.n and 0 <= j < self.m:
            return True
        return False
    
    def is_taller(self, i, j):
        return self.grid[i, j] >= self.grid[self.i, self.j]

    def stop_search(self, i, j):
        if not self.valid_index(i, j):
            return True
        if self.grid[i, j] >= self.grid[self.i, self.j]:
            return True
        return False

    @property
    def scenic_score(self):
        return self.u * self.d * self.l * self.r

def load_grid(path: str) -> np.ndarray:
    with open(path) as f:
        lines = f.read().splitlines()
    grid = np.array([[int(c) for c in l] for l in lines])
    return grid

def print_grid(grid):
    for l in grid:
        print(''.join([str(x) for x in l]))

def print_grid_visibility(grid: np.ndarray, visible: np.ndarray) -> None:
    n, m = grid.shape
    for i in range(n):
        for j in range(m):
            if visible[i,j]:
                print(f"{bcolors.OKGREEN}{grid[i,j]}{bcolors.ENDC}", end='')
                # print(f"{grid[i,j]}", end='')
            else:
                print(f"{bcolors.FAIL}{grid[i,j]}{bcolors.ENDC}", end='')
                # print(f"{grid[i,j]}", end='')
        print()
    print()

def visible_trees(grid):
    n, m = grid.shape
    visible = np.zeros_like(grid)
    visible[0] = 1
    visible[-1] = 1
    visible[:,0] = 1
    visible[:,-1] = 1
    
    down_max = np.zeros(m)
    up_max = np.zeros(m)
    for i in range(n):
        visible[i] |= grid[i] > down_max
        down_max = np.maximum(down_max, grid[i])

        visible[-i-1] |= grid[-i-1] > up_max
        up_max = np.maximum(up_max, grid[-i-1])

    right_max = np.zeros(n)
    left_max = np.zeros(n)
    for j in range(m):
        visible[:,j] |= grid[:,j] > right_max
        right_max = np.maximum(right_max, grid[:,j])

        visible[:,-j-1] |= grid[:,-j-1] > left_max
        left_max = np.maximum(left_max, grid[:,-j-1])
    
    return visible

def get_scenic_score(grid: np.ndarray):
    scenic = np.zeros_like(grid)
    n, m = grid.shape
    for i in range(n):
        for j in range(m):
            if grid[i,j] == 0: continue
            g = GridIterator(grid, i, j)
            scenic[i,j] = g.calculate_scenic_score()
    return scenic

grid = load_grid('day08-input')
# grid = load_grid('tmp')
visible = visible_trees(grid)
scenic = get_scenic_score(grid)
print_grid_visibility(grid, visible)
print(f'Number of visible trees from outside grid: {np.sum(visible)}')
print(scenic)
print(f'Highest scenic score: {np.max(scenic)}')
