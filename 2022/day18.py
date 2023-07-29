import numpy as np

PointCloud = set[tuple[int, int, int]]

def load_points(path: str) -> PointCloud:
    with open(path) as f:
        lines = f.read().splitlines()
    points = {tuple(int(x) for x in line.split(",")) for line in lines}
    return points

def load_point_array(path: str) -> PointCloud:
    with open(path) as f:
        lines = f.read().splitlines()
    points = np.array([[int(x) for x in line.split(",")] for line in lines])
    return points

def num_exposed_faces(points: PointCloud) -> int:
    n = len(points) * 6
    n_adjacent = 2 * (
        sum(int((x - 1, y, z) in points) for (x, y, z) in points)
        + sum(int((x, y - 1, z) in points) for (x, y, z) in points)
        + sum(int((x, y, z - 1) in points) for (x, y, z) in points)
    )
    return n - n_adjacent

def point_bounds(points: PointCloud, pad: int=0):
    xmin = min(x for (x,_,_) in points) - pad
    xmax = max(x for (x,_,_) in points) + pad
    ymin = min(y for (_,y,_) in points) - pad
    ymax = max(y for (_,y,_) in points) + pad
    zmin = min(z for (_,_,z) in points) - pad
    zmax = max(z for (_,_,z) in points) + pad
    return (xmin,ymin,zmin), (xmax,ymax,zmax)

def get_droplet(points: np.ndarray) -> int:
    min_bounds = np.min(points, axis=0) - 1
    max_bounds = np.max(points, axis=0) + 2
    nx, ny, nz = max_bounds - min_bounds 
    droplet = np.zeros((nx, ny, nz), dtype=int)
    for x, y, z in points - min_bounds:
        droplet[x, y, z] = 1
    return droplet

class LavaDroplet:
    def __init__(self, path: str) -> None:
        self.points = load_point_array(path)
        self.droplet = get_droplet(self.points)    
        nx, ny, nz = self.droplet.shape
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.steam = np.zeros_like(self.droplet)
        self.steam_source = (0,0,0)
        self.num_calls = dict()
    
    def out_of_bounds(self, point: tuple[int, int, int]) -> bool:
        x, y, z = point
        if x < 0 or x >= self.nx:
            return True
        if y < 0 or y >= self.ny:
            return True
        if z < 0 or z >= self.nz:
            return True
        return False
    
    def neighbors(self, point: tuple[int, int, int]):
        x, y, z = point
        yield x-1, y, z
        yield x+1, y, z
        yield x, y-1, z
        yield x, y+1, z
        yield x, y, z-1
        yield x, y, z+1


    def __recur(self, point: tuple[int, int, int]) -> int:
        if self.out_of_bounds(point):
            return 0
        if self.steam[point]:
            return 0
        if self.droplet[point]:
            if point in self.num_calls:
                self.num_calls[point] += 1
            else:
                self.num_calls[point] = 1
            return 1
        
        self.steam[point] = 1
        return sum(self.__recur(p) for p in self.neighbors(point))

    def exterior_surface(self) -> int:
        exterior_faces = 0
        point_queue = [self.steam_source]
        while point_queue:
            point = point_queue.pop(0)
            if self.out_of_bounds(point):
                continue
            if self.steam[point]:
                continue
            if self.droplet[point]:
                exterior_faces += 1
                continue
            self.steam[point] = 1
            point_queue.extend(self.neighbors(point))
        return exterior_faces
    
    def __str__(self) -> str:
        layers = []
        for z in range(self.nz):
            lines = []
            for y in range(self.ny):
                line = []
                for x in range(self.nx):
                    c = '.'
                    if self.droplet[x,y,z]:
                        c = str(self.num_calls.get((x,y,z), 0))#'#'
                    if self.steam[x,y,z]:
                        c = '~'
                    line.append(c)
                lines.append(''.join(line))
            layers.append('\n'.join(lines))
        return '\n\n'.join(layers)

points = load_points("day18-input")
print("Number of exposed faces:", num_exposed_faces(points))
lava = LavaDroplet("day18-input")
exterior_faces = lava.exterior_surface()
print("Number of exterior faces:", exterior_faces)