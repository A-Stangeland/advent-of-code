import re


class Stacks:
    def __init__(self, path, n_stacks=9):
        self.n_stacks = n_stacks
        self.stacks = [[] for i in range(self.n_stacks)]
        self._read_file(path)
        self._init_stacks()

    def _read_file(self, path):
        with open(path) as f:
            lines = f.read().splitlines()
        self.initial_stack_lines = lines[:8]
        self.moves = lines[10:]
        # self.initial_stack_lines = lines[:3]
        # self.moves = lines[5:]

    def _init_stacks(self):
        for l in self.initial_stack_lines[::-1]:
            for i, c in enumerate(l[1::4]):
                if c != " ":
                    self.stacks[i].append(c)

    def move(self, n, i1, i2):
        remainder, to_move = self.stacks[i1][:-n], self.stacks[i1][-n:]
        self.stacks[i1] = remainder
        self.stacks[i2].extend(to_move)
        # remainder, to_move = self.stacks[i1][:-1], self.stacks[i1][-1:]
        # self.stacks[i1] = remainder
        # self.stacks[i2].extend(to_move)

    def execute_moves(self, n_moves=None):
        moveset = self.moves if n_moves is None else self.moves[:n_moves]
        for i, line in enumerate(moveset):
            print(i, line)
            n, i1, i2 = [int(x) for x in re.findall("[0-9]+", line)]
            self.move(n, i1 - 1, i2 - 1)
            print(self)

    @property
    def max_len(self):
        return max([len(s) for s in self.stacks])

    def print_top(self):
        for s in self.stacks:
            print(s[-1], end="")
        print()

    def __str__(self):
        lines = ["".join(f" {i+1} " for i in range(self.n_stacks))]
        for level in range(self.max_len):
            line = []
            for i in range(self.n_stacks):
                try:
                    s = f"[{self.stacks[i][level]}]"
                except IndexError:
                    s = "   "
                line.append(s)
            lines.append(" ".join(line))
        return "\n".join(lines[::-1])


s = Stacks("day05-input")
# s = Stacks('tmp', 3)
print(s)
s.execute_moves()
s.print_top()
