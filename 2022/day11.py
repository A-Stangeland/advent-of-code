from typing import Sequence, Iterable
from functools import reduce


class Operation:
    def __init__(self, expression) -> None:
        self.expression = expression
        left, op, right = expression[19:].split(" ")
        self.left = "x" if left == "old" else int(left)
        self.right = "x" if right == "old" else int(right)
        if op == "+":
            self.op = lambda a, b: a + b
        elif op == "*":
            self.op = lambda a, b: a * b

    def __call__(self, x: int):
        left = x if self.left == "x" else self.left
        right = x if self.right == "x" else self.right
        return self.op(left, right)

    def __str__(self) -> str:
        return self.expression


class Test:
    def __init__(self, expression: Sequence[str]) -> None:
        self.expression = expression
        self.divisor = int(expression[0][21:])
        self.if_true = int(expression[1][29:])
        self.if_false = int(expression[2][30:])

    def __call__(self, n: int):
        if n % self.divisor == 0:
            return self.if_true
        else:
            return self.if_false

    def __str__(self) -> str:
        return "\n".join(self.expression) + "\n"


class Monkey:
    def __init__(
        self,
        troop: "Troop",
        n: int,
        starting_items: Iterable[int],
        operation: Operation,
        test: Test,
    ) -> None:
        self.troop = troop
        self.n = n
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.num_inspected = 0

    def inspect(self):
        while len(self.items) > 0:
            item = self.items.pop(0)
            item = self.operation(item) % self.troop.common_divisor
            self.num_inspected += 1
            self.test_item(item)

    def test_item(self, item):
        to_n = self.test(item)
        to_monkey = self.troop.monkeys[to_n]
        self.throw(item, to_monkey)

    def throw(self, item, other: "Monkey"):
        other.items.append(item)

    def __str__(self) -> str:
        lines = [
            f"Monkey {self.n}:",
            f" Items: {', '.join([str(i) for i in self.items])}",
            str(self.operation),
            str(self.test),
        ]
        return "\n".join(lines) + "\n"


class Troop:
    def __init__(self, path) -> None:
        self.monkeys: Sequence[Monkey] = []
        self.populate(path)
        self.common_divisor = self.find_common_divisor()
        self.round_count = 0

    def populate(self, path):
        with open(path) as f:
            lines = f.read().splitlines()
        while lines:
            n = int(lines[0][7])
            starting_items = [int(item) for item in lines[1][18:].split(", ")]
            operation = Operation(lines[2])
            test = Test(lines[3:6])
            new_monkey = Monkey(self, n, starting_items, operation, test)
            self.monkeys.append(new_monkey)
            lines = lines[7:]

    def find_common_divisor(self) -> int:
        return reduce(lambda a, b: a * b, [m.test.divisor for m in self.monkeys])

    def rounds(self, n, print_rounds=None):
        if print_rounds is None:
            print_rounds = []
        for _ in range(n):
            for monkey in self.monkeys:
                monkey.inspect()
            self.round_count += 1
            if self.round_count in print_rounds:
                self.print_num_inspected()

    def print_num_inspected(self):
        print(f"== After round {self.round_count} ==")
        for m in self.monkeys:
            print(f"Monkey {m.n} inspected items {m.num_inspected} times.")
        print()

    @property
    def monkey_business(self):
        num_inspected = sorted([m.num_inspected for m in self.monkeys])
        return num_inspected[-1] * num_inspected[-2]

    def __str__(self) -> str:
        return "\n".join(str(m) for m in self.monkeys) + "\n"


troop = Troop("day11-input")
print(troop)
troop.rounds(10000, print_rounds=[10000])
print(troop.monkey_business)
