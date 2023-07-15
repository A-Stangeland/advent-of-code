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


def load_grid(path: str) -> np.ndarray:
    with open(path) as f:
        lines = f.read().splitlines()
    grid = np.array([[int(c) for c in l] for l in lines])
    return grid

def print_grid(grid: np.ndarray, visible: np.ndarray) -> None:
    # for l in grid:
    #     print(''.join([str(x) for x in l]))

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

grid = load_grid('day08-input')
# grid = load_grid('tmp')
visible = visible_trees(grid)
print_grid(grid, visible)
# print_grid(visible)
print(np.sum(visible))