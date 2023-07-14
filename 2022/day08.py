import numpy as np

def load_grid(path: str) -> np.ndarray:
    with open(path) as f:
        lines = f.read().splitlines()
    grid = np.array([[int(c) for c in l] for l in lines])
    return grid

def print_grid(grid: np.ndarray) -> None:
    for l in grid:
        for x in l:
            print(''.join([str(x) for x in l]))

def visible_trees(grid):
    visible = np.zeros_like(grid)
    visible[0] = 1
    visible[-1] = 1
    visible[:,0] = 1
    visible[:,-1] = 1

grid = load_grid('day08-input')
print_grid(grid)