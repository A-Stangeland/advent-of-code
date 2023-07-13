from typing import Self, Optional

class Directory:
    def __init__(self, name: str, parent: Optional[Self]) -> None:
        self.name = name
        self._parent = parent
        self.children = []

    @property
    def parent(self) -> Self:
        if self._parent is None:
            raise FileNotFoundError(f'{self.name} has no parent directory.')
        return self._parent

    @property
    def size(self) -> int:
        total_size = 0
        for child in self.children:
            total_size += child.size
        return total_size
    
    def print(self, level: int) -> None:
        print(2*level*' ' + f'- {self.name} (dir, size={self.size})')
        for child in self.children:
            child.print(level+1)
    
    def get_small_dirs(self, threshold: int) -> tuple[int, list[int]]:
        total_size = 0
        small_dirs = []
        for child in self.children:
            if isinstance(child, File):
                total_size += child.size
                continue
            child_size, child_small_dirs = child.get_small_dirs(threshold)
            total_size += child_size
            small_dirs.extend(child_small_dirs)
        if total_size <= threshold:
            small_dirs.append(total_size)
        return total_size, small_dirs
    
    def get_sizes(self) -> tuple[int, list[int]]:
        total_size = 0
        dir_sizes = []
        for child in self.children:
            if isinstance(child, File):
                total_size += child.size
                continue
            child_size, child_dir_sizes = child.get_sizes()
            total_size += child_size
            dir_sizes.extend(child_dir_sizes)
        dir_sizes.append(total_size)
        return total_size, dir_sizes

class File:
    def __init__(self, name: str, parent: Directory, size: int=0) -> None:
        self.name = name
        self.parent = parent
        self.size = size
    
    def print(self, level: int) -> None:
        print(2*level*' ' + f'- {self.name} (file, size={self.size})')

class FileExplorer:
    def __init__(self) -> None:
        self.root = Directory('/', None)
        self.cwd = self.root
    
    def cd(self, path) -> None:
        if path == '..':
            self.cwd = self.cwd.parent
            return
        if path == '/':
            self.cwd = self.root
            return
        for child in self.cwd.children:
            if child.name == path:
                self.cwd = child
                return
        raise FileNotFoundError(f'No such file or directory: {path} in {self.cwd.name}')
    
    def ls(self):
        for child in self.cwd.children:
            if isinstance(child, Directory):
                print(f'dir {child.name}')
            else:
                print(f'{child.size} {child.name}')
    
    def touch(self, name: str, size: int):
        new_file = File(name, self.cwd, size)
        self.cwd.children.append(new_file)
    
    def mkdir(self, name: str):
        new_dir = Directory(name, self.cwd)
        self.cwd.children.append(new_dir)
    
    def print_tree(self):
        self.root.print(0)
    
    def sum_under_threshold(self, threshold):
        total_size, small_dirs = self.root.get_small_dirs(threshold)
        return small_dirs


    def find_smallest_to_delete(self):
        total_size, dir_sizes = self.root.get_sizes()
        free_space = 70_000_000 - total_size
        space_needed = 30_000_000 - free_space
        print(f'{total_size=} {free_space=} {space_needed=}')
        for dir_size in sorted(dir_sizes):
            if dir_size >= space_needed:
                print(dir_size)
                return dir_size

def construct_file_tree(path):
    with open(path) as f:
        lines = f.read().splitlines()
    
    explorer = FileExplorer()
    while lines:
        line = lines.pop(0)
        print(line)
        if line[0] == '$':
            command = line[2:4]
            if command == 'cd':
                argument = line[5:]
                explorer.cd(argument)
            continue
        size_or_dir, name = line.split(' ')
        if size_or_dir == 'dir':
            explorer.mkdir(name)
        else:
            explorer.touch(name, int(size_or_dir))
    explorer.print_tree()
    explorer.find_smallest_to_delete()

construct_file_tree('day07-input')

        
